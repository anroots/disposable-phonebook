import threading
import time

from tqdm import tqdm

from dphonebook.phonebook import Phonebook


class Progress:

    progress_bar: tqdm
    providers_count: int = 1

    def __init__(self, phonebook: Phonebook) -> None:
        self.phonebook = phonebook
        self.providers_count = len(phonebook.providers) if phonebook.providers else 1

    def progress(self) -> float:
        total = 0

        for provider in self.phonebook.providers:
            total += provider.progress()
        return round(total / self.providers_count, 2)

    def close(self):
        self.progress_bar.close()

    def print(self):
        previous_progress = 0
        while True:
            current_progress = self.progress()
            self.progress_bar.update(current_progress - previous_progress)
            if current_progress >= 100:
                self.progress_bar.close()
                return
            previous_progress = current_progress
            time.sleep(0.1)

    def monitor(self):
        self.progress_bar = tqdm(total=100, mininterval=0.1)
        thread = threading.Thread(target=self.print, name='thread-progress')
        thread.start()
