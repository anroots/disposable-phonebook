import json
import logging
import queue
import threading
import time

import pkg_resources
from requests import Session

from dphonebook.lib.phonenumber import PhoneNumber
from dphonebook.lib.phonenumber import PhoneNumberJsonEncoder
from dphonebook.lib.writer.result_writer import ResultWriter


class RequestSender(threading.Thread):
    def __init__(self, work_queue: queue.Queue, session: Session, webhook_url: str, logger: logging.Logger, *args, **kwargs):
        self.work_queue = work_queue
        self.session = session
        self.webhook_url = webhook_url
        self.logger = logger
        super().__init__(*args, **kwargs)

    def run(self):
        while True:
            time.sleep(1)

            try:
                work = self.work_queue.get(timeout=3)
            except queue.Empty:
                continue
            if work is None:
                self.work_queue.task_done()
                return
            post_data = json.dumps({'numbers': work}, cls=PhoneNumberJsonEncoder)
            response = self.session.post(self.webhook_url, data=post_data)
            self.logger.info(
                'POST %d items to %s, response status code %d',
                len(work),
                self.webhook_url,
                response.status_code
            )
            if not response.ok:
                self.logger.error(response.content)

            self.work_queue.task_done()


class WebhookWriter(ResultWriter):
    page_size: int = 100
    url: str = ''

    work_queue = queue.Queue
    worker: RequestSender

    def __init__(self, args: dict, logger: logging.Logger) -> None:
        super().__init__(args)
        self.logger = logger
        self.url = self.args.get('url')
        self.page_size = int(self.args.get('page_size', 100))

        if not self.url:
            raise Exception('Invalid URL given to WebhookWriter')

        self.work_queue = queue.Queue()

        RequestSender(
            self.work_queue,
            self.create_session(self.args.get('authorization')),
            self.url,
            logger
        ).start()

    def create_session(self, authorization: str) -> Session:
        session = Session()

        lib_version = pkg_resources.get_distribution('disposable-phonebook').version
        session.headers.update({
            'User-Agent': f'disposable-phonebook/{lib_version}',
            'Content-Type': 'application/json'
        })
        if authorization:
            session.headers.update({'Authorization': authorization})
        return session

    def append(self, number: PhoneNumber):
        super().append(number)

        # Put {page_size} of Numbers into the batch HTTP request queue
        if len(self.results) > self.page_size:
            self.work_queue.put(self.results[0:self.page_size])
            del self.results[0:self.page_size]

    def write(self):
        # Any leftover Numbers to process (less than {page_size})
        self.work_queue.put(self.results)

        # This tell worker thread to exit
        self.work_queue.put(None)

        self.work_queue.join()
