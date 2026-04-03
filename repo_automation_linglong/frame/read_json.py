# -*- coding: utf-8 -*-
"""
@Time ： 2021/6/11 上午10:33
@Auth ： zhanyuanyuan
@File ：read_json.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
import json


def get_read_json(test_data_path):
    data_file=[]
    if test_data_path:
        with open(test_data_path,encoding="utf-8") as f:
            test_data=json.loads(f.read())
    else:
        raise Exception("data was not prepared")
    data_list=test_data["test"]
    for date_case in data_list:
        requests=tuple([date_case["expected"],date_case['http']["url"],date_case['http']["headers"],date_case["casename"]])
        data_file.append(requests)
    return data_file


def post_read_json(test_data_path):
    data_file = []
    if test_data_path:
        with open(test_data_path, encoding="utf-8") as f:
            test_data = json.loads(f.read())
    else:
        raise Exception("data was not prepared")
    data_list = test_data['test']
    for date_case in data_list:
        requests = tuple([date_case["expected"], date_case['http']["url"], date_case['http']["headers"],
                          date_case['http']["data"],date_case["casename"]])
        data_file.append(requests)

    return tuple(data_file)


# if __name__ == "__main__":
#     # von = Read_Json("/home/lizhouquan/Desktop/py_learn/uniontest-master/deepin-elf-sign-tool/data/web_oauth2/center_1.json")
#     # von.get_read_json()
#     test_data_path="/home/lizhouquan/Desktop/py_learn/uniontest-master/deepin-elf-sign-tool/data/web_oauth2/center_1.json"
#     gg=get_read_json(test_data_path)







