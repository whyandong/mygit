# -*- coding: utf-8 -*-
"""
@Time ： 2021/6/22 下午4:49
@Auth ： lizhouquan
@File ：anasyls.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)

"""
def get_state(key,val):
    """
    解析返回体中的URL中代的参数值
    :param key: 参数值key
    :param val: 解析的对象
    :return:
    """
    return_data = None
    init_data = val.split("?")[1]
    key_val_data = init_data.split("&")
    Flag = True
    i = 0
    while Flag:
        if i < len(key_val_data):
            if key == key_val_data[i].split("=")[0]:
                return_data = key_val_data[i].split("=")[1]
                Flag = False
            else:
                i += 1
    return return_data