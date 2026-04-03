# -*- coding: utf-8 -*-
import logging
import dbus

from aw.dbus.dbus_common import get_session_dbus_interface
from aw.dbus.sessionBus import sessionCommon
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.api.Pinyin'
DBUS_PATH = '/com/deepin/api/Pinyin'
IFACE_NAME = 'com.deepin.api.Pinyin'


def dbus_interface():
    return get_session_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


@checkword
def queryPinyin(hans):
    """
    查询输入的汉字hans的拼音
    :param hans: 汉字，包含字和词
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.Query(hans)
    if isinstance(result, dbus.Array):
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据不是Array:{type(result)}')
        return False


@checkword
def QueryList(hans_list):
    """
    查询输入的汉字hans的拼音，支持查询多组汉字词
    :param hans_list: 需要查询的汉字，为一个列表
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.QueryList(hans_list)
    if isinstance(result, dbus.String):
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据不是Array:{type(result)}')
        return False
