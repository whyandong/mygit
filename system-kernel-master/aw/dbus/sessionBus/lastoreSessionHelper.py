# -*- coding: utf-8 -*-
import logging
import dbus

from aw.dbus.dbus_common import get_session_dbus_interface
from aw.dbus.sessionBus import sessionCommon
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.LastoreSessionHelper'
DBUS_PATH = '/com/deepin/LastoreSessionHelper'
IFACE_NAME = 'com.deepin.LastoreSessionHelper'


def dbus_interface():
    return get_session_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


@checkword
def isDiskSpaceSufficient():
    """
    判断磁盘是否有剩余的空间
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.IsDiskSpaceSufficient()
    if isinstance(result, dbus.Boolean):
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据不是Boolean:{type(result)}')
        return False
