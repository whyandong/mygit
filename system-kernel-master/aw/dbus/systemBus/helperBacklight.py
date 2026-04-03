# -*- coding: utf-8 -*-
import logging

from frame.decorator import checkword
from aw.dbus.systemBus import systemCommon

dbus_name = 'com.deepin.daemon.helper.Backlight'
dbus_path = '/com/deepin/daemon/helper/Backlight/DDCCI'
iface_name = 'com.deepin.daemon.helper.Backlight.DDCCI'


@checkword
def refreshDisplays():
    """
    刷新显示设备列表
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    out = property_obj.RefreshDisplays()
    logging.info(out)
    if not out:
        logging.info("刷新显示设备列表成功")
        return True
    else:
        logging.info("刷新显示设备列表失败")
        return False
