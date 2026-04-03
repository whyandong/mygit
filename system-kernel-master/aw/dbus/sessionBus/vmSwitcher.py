# -*- coding: utf-8 -*-
import dbus
import time
import logging

from aw.dbus.sessionBus import sessionCommon
from frame.decorator import checkword

dbus_name = 'com.deepin.WMSwitcher'
dbus_path = '/com/deepin/WMSwitcher'
iface_name = 'com.deepin.WMSwitcher'


@checkword
def allowSwitch():
    """
    是否允许切换窗口管理器，其实是是否允许切换窗口特效的开关。
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.AllowSwitch()
    logging.info(result)
    if isinstance(result, dbus.Boolean):
        logging.info(f"获取窗口特效的开关状态值{result}成功")
        return True
    else:
        logging.info("获取窗口特效的开关状态值失败")
        return False


@checkword
def currentWM():
    """
    获取当前窗口管理器，其实是获取当前窗口特效模式，2D时返回 deepin metacity, 3D 时返回 deepin wm。
    :return:True or False
    """
    result = getCurrentWM()
    logging.info(result)
    if isinstance(result, dbus.String):
        logging.info(f"获取当前窗口特效模式为{result}成功")
        return True
    else:
        logging.info("获取当前窗口特效模式失败")
        return False


def getCurrentWM():
    """
    获取当前窗口管理器，其实是获取当前窗口特效模式，2D时返回 deepin metacity, 3D 时返回 deepin wm。
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.CurrentWM()
    return result


@checkword
def requestSwitchWM():
    """
    请求切换窗口管理器，其实是切换窗口特效
    :return:None
    """
    vm1 = getCurrentWM()
    logging.info(f"窗口特效模式为{vm1}")
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    property_obj.RequestSwitchWM()
    time.sleep(2)
    vm2 = getCurrentWM()
    logging.info(f"切换窗口特效模式为{vm2}")
    if vm1 != vm2:
        logging.info("检查切换窗口特效成功")
        return True
    else:
        logging.info("切换窗口特效失败")
        return False

def resetSwitchWM():
    """
    恢复特效默认模式为2D
    :return:None
    """
    vm1 = getCurrentWM()
    logging.info(f"当前窗口特效模式为{vm1}")

    if "deepin wm" not in vm1:
        property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
        property_obj.RequestSwitchWM()
        time.sleep(2)
        vm2 = getCurrentWM()
        logging.info(f"恢复窗口特效模式为{vm2}")

if __name__ == "__main__":
    import sys

    I_g = logging.getLogger()
    I_g.setLevel(logging.DEBUG)
    s_h = logging.StreamHandler(sys.stdout)
    I_g.addHandler(s_h)
    resetSwitchWM()
