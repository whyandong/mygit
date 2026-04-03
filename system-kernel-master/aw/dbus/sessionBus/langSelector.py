# -*- coding: utf-8 -*-
import logging
from time import sleep

import dbus

from aw.dbus.dbus_common import get_session_dbus_interface
from aw.dbus.sessionBus import sessionCommon
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.daemon.LangSelector'
DBUS_PATH = '/com/deepin/daemon/LangSelector'
IFACE_NAME = 'com.deepin.daemon.LangSelector'


def dbus_interface():
    return get_session_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


def getLocale():
    """
    获取语言环境选项参数
    :return: 语言环境选项参数:locale
    """
    interface = dbus_interface()
    result = interface.GetLocaleList()
    locale = result[1][0]
    logging.info(locale)
    return locale


@checkword
def getLocaleList():
    """
    获取系统支持的语言环境信息列表
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.GetLocaleList()
    if isinstance(result, dbus.Array):
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据不是Array:{type(result)}')
        return False


@checkword
def addLocale(locale):
    """
    增加系统语言环境选项
    :param locale: 语言环境选项,参数值参照’/etc/locale.gen‘文件中的内容
    :return: True or False
    """
    interface = dbus_interface()
    interface.AddLocale(locale)
    logging.info("检查接口执行成功")
    return True


@checkword
def deleteLocale(locale):
    """
    删除系统语言环境选项
    :param locale: 语言环境选项,参数值参照’/etc/locale.gen‘文件中的内容
    :return: True or False
    """
    interface = dbus_interface()
    langSelectorReset()
    sleep(3)
    interface.DeleteLocale(locale)
    logging.info("检查接口执行成功")
    return True


@checkword
def getLanguageSupportPackages(locale):
    """
    获取对应语言环境的语言支持包
    :param locale: 语言环境选项,参数值参照’/etc/locale.gen‘文件中的内容
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.GetLanguageSupportPackages(locale)
    if isinstance(result, dbus.Array):
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据不是Array:{type(result)}')
        return False


@checkword
def getLocaleDescription(locale):
    """
    获取对应语言环境的描述
    :param locale: 语言环境选项,参数值参照’/etc/locale.gen‘文件中的内容
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.GetLocaleDescription(locale)
    if isinstance(result, dbus.String):
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据不是String:{type(result)}')
        return False


@checkword
def langSelectorReset():
    """
    将设置的用户桌面语言环境重置为系统默认语言环境
    :return: True or False
    """
    interface = dbus_interface()
    interface.Reset()
    sleep(10)
    logging.info("检查接口执行成功")
    return True


@checkword
def setLocale(locale):
    """
    设置当前用户的桌面语言环境
    :param locale: 语言环境选项,参数值参照’/etc/locale.gen‘文件中的内容
    :return: True or False
    """
    interface = dbus_interface()
    interface.SetLocale(locale)
    langSelectorReset()
    sleep(10)
    logging.info("检查接口执行成功")
    return True



@checkword
def getLocales():
    """
    获取当前语言环境列表的内容
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.LangSelector', 'Locales')
    logging.info(result)
    if isinstance(result, dbus.Array):
        logging.info("获取当前语言环境列表的内容成功")
        return True
    else:
        logging.info(f'返回数据不是Array:{type(result)}')
        return False


@checkword
def getLocaleState():
    """
    获取存储当前语言环境的状态  0:语言环境切换完成  1:语言环境正在切换中
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.LangSelector', 'LocaleState')
    logging.info(result)
    if isinstance(result, dbus.Int32):
        logging.info("获取存储当前语言环境的状态成功")
        return True
    else:
        logging.info("获取存储当前语言环境的状态失败")
        return False


@checkword
def getCurrentLocale():
    """
    获取当前用户的桌面语言环境
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.LangSelector', 'CurrentLocale')
    logging.info(result)
    if isinstance(result, dbus.String):
        logging.info("获取当前用户的桌面语言环境成功")
        return True
    else:
        logging.info("获取当前用户的桌面语言环境失败")
        return False

