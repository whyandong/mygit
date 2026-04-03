# -*- coding: utf-8 -*-
import logging
import dbus

from aw.dbus.dbus_common import get_session_dbus_interface
from aw.dbus.sessionBus import sessionCommon
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.daemon.SessionWatcher'
DBUS_PATH = '/com/deepin/daemon/SessionWatcher'
IFACE_NAME = 'com.deepin.daemon.SessionWatcher'


def dbus_interface():
    return get_session_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


@checkword
def getSessions():
    """
    获取所有Sessions的对象路径
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.GetSessions()
    if isinstance(result, dbus.Array):
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据不是Array:{type(result)}')
        return False


@checkword
def isX11SessionActive():
    """
    X11 Session是否活跃
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.IsX11SessionActive()
    if isinstance(result, dbus.Boolean):
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据不是Boolean:{type(result)}')
        return False


@checkword
def getIsActive():
    """
    是否存在着活跃Session，返回Boolean类型数据
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.SessionWatcher', 'IsActive')
    logging.info(result)
    if isinstance(result, dbus.Boolean):
        logging.info("检查是否存在着活跃Session")
        return True
    else:
        logging.info("检查是否存在着活跃Session")
        return False
