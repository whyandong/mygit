# -*- coding: utf-8 -*-
import logging

from aw.dbus.sessionBus import sessionCommon
from frame.decorator import checkword

dbus_name = 'com.deepin.daemon.Display'
dbus_path = '/com/deepin/daemon/Display'
iface_name = 'com.deepin.daemon.Display'


@checkword
def getRealDisplayMode():
    """
    获取显示器真实排列方式
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    dbus_out = property_obj.GetRealDisplayMode()
    logging.info(dbus_out)
    if dbus_out:
        logging.info('获取显示器真实排列方式成功')
        return True
    else:
        logging.info('获取显示器真实排列方式失败')
        return False
