# -*- coding: utf-8 -*-
"""
@Time ： 2021/6/23 上午10:38
@Auth ： lizhouquan
@File ：read_config.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)

"""
import configparser
import os
crrent_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def get_values_from_config(key,cmd="public",config_path=crrent_path+"/conf/config.ini"):
    """
    从配置文件中读取指定的值
    :param key: 需要读取的配置文件的key
    :param cmd: 需要读取的配置文件部分的值，默认读取public部分
    :param config_path: 配置文件默认的路径信息
    :return: 返回指定的值
    """
    config = configparser.ConfigParser()
    config.read(config_path)
    return config.get(cmd,key)

if __name__ == '__main__':
    cmd = "user_info"
    ps = get_values_from_config(cmd=cmd,key="account")
    print(ps)
