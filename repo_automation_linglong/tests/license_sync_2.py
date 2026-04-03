# -*- coding:utf8 -*
import pytest

from frame.sha256 import method_256
import time
import json
import random
import requests

#status错误
if __name__ == '__main__':
    url = "http://gray-update-pre.uniontech.com/api/v1/license/sync"
    shu_id = "zzazzz" + str(random.randint(1, 10000000))
    name = "test" + str(random.randint(1, 10000))
    message = str(random.randint(1, 9999999))
    data = [
        {
            "license_machine_id": shu_id,
            "status": 1,
            "customer_name": name,
            "message_id": message
        }
    ]
    headers = {
        'Content-Type': 'application/json'
    }

    dataStr = json.dumps(data, separators=(',', ':'))
    # 生成token
    # print(dataStr)
    token = method_256(dataStr.encode('utf-8').decode('unicode-escape'))
    # print(token)
    rt = str(int(time.time()))
    url = "{0}?token={1}&rt={2}".format(url, token, rt)
    result = requests.post(url=url, headers=headers, data=dataStr)
    reps = result.json()





