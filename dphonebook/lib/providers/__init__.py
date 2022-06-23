from dphonebook.lib.providers.dummy_example_com import DummyExampleCom
from dphonebook.lib.providers.receive_sms_co import ReceiveSmsCo
from dphonebook.lib.providers.receive_sms_online_info import ReceiveSmsOnlineInfo
from dphonebook.lib.providers.receive_sms_org import ReceiveSmsOrg
from dphonebook.lib.providers.receive_smss import ReceiveSmss
from dphonebook.lib.providers.sms_online_co import SmsOnlineCo


number_provider_classes = [
    DummyExampleCom,
    ReceiveSmss,
    ReceiveSmsCo,
    ReceiveSmsOnlineInfo,
    ReceiveSmsOrg,
    SmsOnlineCo
]
