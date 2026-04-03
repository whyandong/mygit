# -*- coding: utf-8 -*-
"""
@Time ： 2021/11/3 下午7:32
@Auth ： lizhouquan
@File ：get_uosid.py.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)

"""

from frame.get_public import account_encrypt
from frame.read_json import post_read_json
from frame.constant import bind_unionid
from common_relate.login_authorization import oauth_key
from common_relate.get_uosid import get_uosid
import requests


def get_ubid():
    data_1=post_read_json(bind_unionid)
    datas = data_1[0][3]
    url = data_1[0][1]
    headers = data_1[0][2]
    datas['UOSID']=get_uosid()
    datas['UUID']=account_encrypt(datas['UUID'],oauth_key())
    result = requests.post(url=url,headers=headers,json=datas)
    get_ubid = result.json()
    ubid=get_ubid['data']['UBID']
    return ubid


if __name__ ==  "__main__":
    cc=get_ubid()
    print(cc)


