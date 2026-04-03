# -*- coding: utf-8 -*-
import logging
import dbus

from aw.dbus.dbus_common import get_session_dbus_interface
from aw.dbus.sessionBus import sessionCommon
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.daemon.Mime'
DBUS_PATH = '/com/deepin/daemon/Mime'
IFACE_NAME = 'com.deepin.daemon.Mime'


def start_monitor_signal(member):
    dbus_monitor = sessionCommon.DbusMonitor(DBUS_NAME, DBUS_PATH, member)
    dbus_monitor.start()
    return dbus_monitor


def stop_monitor_signal(dbus_monitor: sessionCommon.DbusMonitor):
    dbus_monitor.stop()


def parse_stop_monitor_signal(dbus_monitor: sessionCommon.DbusMonitor):
    return dbus_monitor.parse()


def dbus_interface():
    return get_session_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


@checkword
def listApps(mime_type):
    """
    获取支持特定mime的所有App信息的Json字符串
    :param mime_type: 特定mime类型
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.ListApps(mime_type)
    if isinstance(result, dbus.String):
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据不是String:{type(result)}')
        return False


@checkword
def listUserApps(mime_type):
    """
    获取支持特定mime的所有用户App信息的Json字符串
    :param mime_type: 特定mime类型
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.ListUserApps(mime_type)
    if isinstance(result, dbus.String):
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据不是String:{type(result)}')
        return False


@checkword
def getDefaultApp(mime_type):
    """
    获取特定mime的默认App
    :param mime_type: 特定mime类型
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.GetDefaultApp(mime_type)
    if isinstance(result, dbus.String):
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据不是String:{type(result)}')
        return False


@checkword
def deleteApp(mime_type, desktop_id):
    """
    删除APP对一系列mime的支持
    :param mime_type: 被删除的mime类型
    :param desktop_id: 被删除mime类型的APP的desktop id
    :return: True or False
    """
    interface = dbus_interface()
    interface.DeleteApp(mime_type, desktop_id)
    logging.info("检查接口执行成功")
    return True


@checkword
def addUserApp(mime_type, desktop_id):
    """
    添加用户App和用户App支持的一系列mime
    :param mime_type:  被添加App支持的mime类型
    :param desktop_id: 被添加的App的desktop id
    :return: True or False
    """
    interface = dbus_interface()
    interface.AddUserApp(mime_type, desktop_id)
    logging.info("检查接口执行成功")
    return True


@checkword
def deleteUserApp(desktop_id):
    """
    删除对默认程序支持的App列表中的某个用户App
    :param desktop_id: 被操作的App的desktop id
    :return: True or False
    """
    interface = dbus_interface()
    interface.DeleteUserApp(desktop_id)
    logging.info("检查接口执行成功")
    return True


@checkword
def setDefaultApp(mime_types, desktop_id):
    """
    为一系列mime设置同一个默认的App
    :param mime_types: 一系列mime类型
    :param desktop_id: 默认App的desktop id
    :return: True or False
    """
    interface = dbus_interface()
    interface.SetDefaultApp(mime_types, desktop_id)
    logging.info("检查接口执行成功")
    return True
