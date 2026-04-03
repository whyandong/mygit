# -*- coding: utf-8 -*-
import logging
import dbus

from aw.dbus.dbus_common import get_session_dbus_interface
from aw.dbus.sessionBus import sessionCommon
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.dde.daemon.Launcher'
DBUS_PATH = '/com/deepin/dde/daemon/Launcher'
IFACE_NAME = 'com.deepin.sync.Config'


def dbus_interface():
    return get_session_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


def getSyncConfig():
    """
    获取配置值
    :return: result
    """
    interface = dbus_interface()
    result = interface.Get()
    logging.info(result)
    return result


@checkword
def launcherSyncConfigGet():
    """
    获取配置信息
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.Get()
    if isinstance(result, dbus.Array):
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据不是Array:{type(result)}')
        return False


@checkword
def launcherSyncConfigSet(data):
    """
    设置配置信息
    :param data: 要保存的配置信息
    :return: True or False
    """
    interface = dbus_interface()
    interface.Set(data)
    logging.info("检查接口执行成功")
    return True
