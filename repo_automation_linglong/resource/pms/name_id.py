# _*_ coding: utf-8 _*_
"""
Time:     21-4-26 下午12:09
Author:   quxiang@uniontech.com
File:     name_id.py
Describe: 域管接口测试自动化
"""
import sys
import os
import re
import json
# s = 'cases/web_udcp/ploy_service/ploy_manager/test_post_usb_add_log_1.py::TestStart::test_delete_policy_group'
# print(os.path.split(s)[1].split('.')[0])
file = '/home/quxiang/Desktop/soluautotest/resource/pms/name2id.json'
#
with open(file, 'r') as f:
    F = f.readline()
    data = json.loads(F)
    # print(data)
    for item in data:
        # print(data[item])
        x = data[item]
        s = item.split("test_")
        item_new = "test_" + s[-1]
        data[item_new] = data.pop(item)
        print(item)
    print(data)

    with open(file, 'w') as f:
        json.dump(data,f)
        f.close()


