# -*- coding: utf-8 -*-
"""
@Time ： 2021/11/3 下午7:32
@Auth ： lizhouquan
@File ：get_uosid.py.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)

"""

from frame.get_public import account_encrypt,encrypt_bytes
from frame.read_json import post_read_json
from frame.constant import get_uosid_path
from common_relate.login_authorization import oauth_key
import requests
import datetime
from io import BytesIO
import uuid
import datetime
import time
from frame.read_config import get_values_from_config
unencrypt_MachineID = get_values_from_config(cmd='user_info',key='MachineID')

def encrypt_MachineID():
    stream =BytesIO()
    stream.write(uuid.uuid4().bytes)
    stream.write("@".encode(encoding='UTF-8',errors='strict'))
    start = datetime.datetime(2021,1,1,0,0,0)
    end = datetime.datetime.now()
    stream.write(int((end-start).total_seconds()).to_bytes(4,"big"))
    stream.write("@".encode(encoding='UTF-8',errors='strict'))
    stream.write(unencrypt_MachineID.encode(encoding='UTF-8',errors='strict'))
    MID=stream.getvalue()
    return MID


def get_uosid():
    data_1=post_read_json(get_uosid_path)
    datas = data_1[0][3]
    url = data_1[0][1]
    datas['MachineID'] = encrypt_bytes(encrypt_MachineID(),oauth_key())

    result = requests.post(url=url,json=datas)
    get_uosid = result.json()
    uosid = get_uosid['data']['UOSID']
    UOSID = account_encrypt(uosid,oauth_key())
    return UOSID



if __name__ ==  "__main__":
    cc=get_uosid()
    print(cc)