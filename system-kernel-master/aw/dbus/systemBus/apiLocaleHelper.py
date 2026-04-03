# -*- coding: utf-8 -*-
import logging

import dbus

from frame.decorator import checkword
from aw.dbus.dbus_common import get_system_dbus_interface, dbus_send_for_system

DBUS_NAME = 'com.deepin.api.LocaleHelper'
DBUS_PATH = '/com/deepin/api/LocaleHelper'
IFACE_NAME = 'com.deepin.api.LocaleHelper'


def dbus_interface():
    return get_system_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


def generate_locale(locale='zh_CN.UTF-8', target=None, passwd='123'):
    """
    按照传入的语言信息生成区域语言
    :param locale: zh_CN.UTF-8、 en_US.UTF-8 等
    :param target: None or error
    :param passwd: 密码, 默认123
    :return:True or False
    """
    dbus_iface_method = f"{IFACE_NAME}.GenerateLocale string:'{locale}'"
    result = dbus_send_for_system(DBUS_NAME, DBUS_PATH, dbus_iface_method, passwd, True)
    logging.info(result)
    if target is None:
        if 'Error' in result:
            return False
        return True
    else:
        if 'Error com.deepin.DBus.Error.Unnamed: invalid locale' in result:
            logging.info('引发了invalid locale错误')
            return True
        return False


def set_locale(locale='zh_CN.UTF-8', target=None, passwd='123'):
    """
     SetLocale (String locale) ↦ ()
    按照语言设置默认的本地语言
    参数
        locale：需要设置的本地语言的语言类型字符串(语言字符串文件可参照：/etc/locale.gen)
    返回
        无
    报错
        invalid locale：locale传入错误将报此错
    :param locale: zh_CN.UTF-8、 en_US.UTF-8 等
    :param target: None or error
    :param passwd: 密码, 默认123
    :return: True or False
    """
    dbus_iface_method = f"{IFACE_NAME}.SetLocale string:'{locale}'"
    result = dbus_send_for_system(DBUS_NAME, DBUS_PATH, dbus_iface_method, passwd, True)
    logging.info(result)
    if target is None:
        if 'Error' in result:
            return False
        return True
    else:
        if 'Error com.deepin.DBus.Error.Unnamed: invalid locale' in result:
            logging.info('引发了invalid locale错误')
            return True
        return False


@checkword
def generateLocale(locale='zh_CN.UTF-8', target=None, passwd=None):
    """
    GenerateLocale (String locale) ↦ ()
    按照传入的语言信息生成区域语言
    参数
        locale：需要生成的区域语言的语言类型字符串(语言字符串可参照：/etc/locale.gen)
    返回
        无
    报错
        invalid locale：locale传入错误将报此错
    :param locale: zh_CN.UTF-8、 en_US.UTF-8 等
    :param target: None or error
    :param passwd: 密码, 默认123
    :return:True or False
    """
    dbus_iface_method = f"{IFACE_NAME}.GenerateLocale string:'{locale}'"
    result = dbus_send_for_system(DBUS_NAME, DBUS_PATH, dbus_iface_method, passwd, True)
    logging.info(result)
    if target is None:
        if 'Error' in result:
            return False
        return True
    else:
        if 'Error com.deepin.DBus.Error.Unnamed: invalid locale' in result:
            logging.info('引发了invalid locale错误')
            return True
        return False


@checkword
def setLocale(locale='zh_CN.UTF-8', target=None, passwd=None):
    """
     SetLocale (String locale) ↦ ()
    按照语言设置默认的本地语言
    参数
        locale：需要设置的本地语言的语言类型字符串(语言字符串文件可参照：/etc/locale.gen)
    返回
        无
    报错
        invalid locale：locale传入错误将报此错
    :param locale: zh_CN.UTF-8、 en_US.UTF-8 等
    :param target: None or error
    :param passwd: 密码, 默认123
    :return: True or False
    """
    dbus_iface_method = f"{IFACE_NAME}.SetLocale string:'{locale}'"
    result = dbus_send_for_system(DBUS_NAME, DBUS_PATH, dbus_iface_method, passwd, True)
    logging.info(result)
    if target is None:
        if 'Error' in result:
            return False
        return True
    else:
        if 'Error com.deepin.DBus.Error.Unnamed: invalid locale' in result:
            logging.info('引发了invalid locale错误')
            return True
        return False


@checkword
def success(dbus_monitor, *parse_flgs: str):
    """
    Success(ok Boolean, reason String)
    设置成功信号
    ok：是否成功，true成功，false失败
    reason：失败原因，如果ok为true，返回空字符串
    :param dbus_monitor: dbus_common.DbusMonitor类的实例,且已运行start
    :param parse_flg:检查用字符串,判断此字符串在不在返回的结果中
    :return:True or False
    """
    result = dbus_monitor.parse()
    for parse_flg in parse_flgs:
        logging.info(f'success parse_flg:\n{parse_flg}')
        logging.info(f'success result:\n{result}')
        if parse_flg in result:
            logging.info('parse_flg在result中')
            return True
        else:
            logging.info('parse_flg不在result,请检查此接口')
            return False
    else:
        return True
