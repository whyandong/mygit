# -*- coding: utf-8 -*-
import logging
import dbus

from aw.dbus.dbus_common import get_session_dbus_interface
from aw.dbus.sessionBus import sessionCommon
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.api.CursorHelper'
DBUS_PATH = '/com/deepin/api/CursorHelper'
IFACE_NAME = 'com.deepin.api.CursorHelper'


def dbus_interface():
    return get_session_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


@checkword
def cursorHelperSet(cursor_name):
    """
    设置光标的主题name
    :param cursor_name: 光标主题名,支持的光标主题在/usr/share/icons/*/cursor.theme中定义
    :return: True or False
    """
    interface = dbus_interface()
    interface.Set(cursor_name)
    logging.info("检查接口执行成功")
    return True
