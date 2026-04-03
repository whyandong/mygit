# -*- coding: utf-8 -*-
import logging
import dbus
import time

from frame.decorator import checkword
from aw.dbus.systemBus import systemCommon
from aw.dbus.dbus_common import get_system_dbus_interface

DBUS_NAME = 'com.deepin.dde.LockService'
DBUS_PATH = '/com/deepin/dde/LockService'
IFACE_NAME = 'com.deepin.dde.LockService'


def dbus_interface():
    return get_system_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


def get_properties_value(properties: str):
    property_obj = get_system_dbus_interface(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(IFACE_NAME, properties)
    return result


@checkword
def authenticateUser(username):
    """
    用户认证
    :param username
    :return:Boolean
    """
    interface = dbus_interface()
    interface.AuthenticateUser(username)
    return True



@checkword
def currentUser():
    """
    通过名称获取加密数据内容
    :param 无
    :return Boolean
    """
    interface = dbus_interface()
    result = interface.CurrentUser()
    logging.info(f'当前用户为:{result}')
    if isinstance(result,dbus.String):
        return True
    else:
        logging.info(f'获取当前用户名返回值类型错误，类型为:{type(result)}')
        return False




@checkword
def isLiveCD(username):
    """
    当前是否是引导盘
    :param:username String
    :return:Boolean
    """
    interface = dbus_interface()
    result = interface.IsLiveCD(username)
    logging.info(f'当前是否为引导盘:{result}')
    if isinstance(result,dbus.Boolean):
        return True
    else:
        logging.info(f'是否为引导盘返回值类型错误，类型为:{type(result)}')
        return False

@checkword
def switchToUser(username):
    """
    切换到用户
    :param username:
    :return:Boolean
    """
    interface = dbus_interface()
    interface.SwitchToUser(username)
    logging.info(f'切换到{username}用户')
    return True


@checkword
def unlockCheck(username,passwd):
    """
    解锁检查
    :param:name Srting
    :param:passwd String
    :return boolean
    """
    interface = dbus_interface()
    interface.UnlockCheck(username,passwd)
    return True
