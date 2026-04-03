# -*- coding: utf-8 -*-
import logging
import dbus

from aw.dbus.dbus_common import get_session_dbus_interface
from aw.dbus.sessionBus import sessionCommon
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.daemon.Search'
DBUS_PATH = '/com/deepin/daemon/Search'
IFACE_NAME = 'com.deepin.daemon.Search'


def dbus_interface():
    return get_session_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


def getSearchWithStrList(str_list):
    """
    创建搜索数据集合，并获取对应的值
    :param str_list: 搜索数据集合（列表类型）
    :return: md5sum: md5值，作为此搜索数据集合的标识符。ok: true 表示创建成功，否则失败。
    """
    interface = dbus_interface()
    result = interface.NewSearchWithStrList(str_list)
    return result


@checkword
def newSearchWithStrDict(data_set):
    """
    通过字符字典进行搜索创建一个搜索数据集合，数据类型是 map[string]string, map 的键是要搜索的目标，值是搜索关键字。
    :param data_set:  搜索数据集合（字典类型）
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.NewSearchWithStrDict(data_set)
    if isinstance(result[0], dbus.String):
        logging.info(result[0])
        if isinstance(result[1], dbus.Boolean):
            logging.info(result[1])
            return True
    else:
        logging.info(f'返回数据错误:{type(result)}')
        return False


@checkword
def newSearchWithStrList(data_list):
    """
    创建一个搜索数据集合，数据类型是字符串列表，列表的每个元素即是搜索的目标，也是搜索的关键字。
    :param data_list: 搜索数据集合（列表类型）
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.NewSearchWithStrList(data_list)
    if isinstance(result[0], dbus.String):
        logging.info(result[0])
        if isinstance(result[1], dbus.Boolean):
            logging.info(result[1])
            return True
    else:
        logging.info(f'返回数据错误:{type(result)}')
        return False


@checkword
def searchStartWithString(word, md5sum):
    """
    进行数据集合的搜索，搜索限制条件简单，只是字符串开头要匹配 str，忽略大小写。
    :param word: 搜索词
    :param md5sum:  搜索数据集合的 md5值
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.SearchStartWithString(word, md5sum)
    if isinstance(result, dbus.Array):
        logging.info(word)
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据不是Array:{type(result)}')
        return False


@checkword
def searchString(word, md5sum):
    """
    进行数据集合的搜索，支持模糊拼音搜索。
    :param word: 搜索词
    :param md5sum:  搜索数据集合的 md5值
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.SearchString(word, md5sum)
    if isinstance(result, dbus.Array):
        logging.info(word)
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据不是Array:{type(result)}')
        return False


