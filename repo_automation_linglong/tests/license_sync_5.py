# -*- coding:utf8 -*
import pytest

from frame.sha256 import method_256
import time
import json

import requests

#message_id为空
if __name__ == '__main__':
    url = "https://gray-update-pre.uniontech.com/api/v1/license/sync"
    data = [
        {
        "license_machine_id":"",
        "status":1,
        "customer_name":"统信软件",
        "message_id":"",
        }
    ]

    headers = {
        'Content-Type': 'application/json'
    }


    dataStr = json.dumps(data, separators=(',', ':'))
    # 生成token
    print(dataStr)
    token = method_256(dataStr.encode('utf-8').decode('unicode-escape'))
    print(token)
    rt = str(int(time.time()))
    url = "{0}?token={1}&rt={2}".format(url, token, rt)


    result = requests.post(url=url,headers=headers,data=dataStr)
    reps = result.json()
    if reps['code'] == 1:
        print("验证通过")
    else:
        print("验证失败")



