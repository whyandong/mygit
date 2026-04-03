# -*- coding: utf-8 -*-
import dbus
import logging
import re
import time

from aw.dbus.sessionBus import sessionCommon
from frame.decorator import checkword

dbus_name = 'com.deepin.dde.osd'
dbus_path = '/com/deepin/dde/Notification'
iface_name = 'com.deepin.dde.Notification'


# @checkword
# def getSystemSetting():
#     """
#     获取声卡信息
#     :return:True or False
#     """
#     property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
#     result = property_obj.Get('com.deepin.daemon.Audio', 'Cards')
#     logging.info(result)
#     if isinstance(result, dbus.String):
#         logging.info("获取声卡信息成功")
#         return True
#     else:
#         logging.info("获取声卡信息失败")
#         return False

@checkword
def getCapbilities():
    """
    获取功能项
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.GetCapbilities()
    logging.info(result)
    if isinstance(result, dbus.Array):
        return True
    else:
        return False


@checkword
def getAppList():
    """
    获取应用名称列表
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.GetAppList()
    logging.info(result)
    if isinstance(result, dbus.Array):
        return True
    else:
        return False


def clearRecords():
    """
    删除所有通知记录
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    ret = property_obj.ClearRecords()
    time.sleep(3)
    return ret


@checkword
def checkClearRecordsStatus():
    """
    检查清除记录成功
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    ret = property_obj.recordCount()
    logging.info(ret)
    if ret == 0:
        return True
    else:
        return False


@checkword
def hide():
    """
    隐藏通知中心
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    property_obj.Hide()
    time.sleep(2)
    return True


@checkword
def getServerInformation():
    """
    获取服务信息
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    ret = property_obj.GetServerInformation()
    logging.info(ret)
    if isinstance(ret, tuple):
        return True
    else:
        return False


@checkword
def getAllRecords():
    """
    返回所有通知的记录
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    ret = property_obj.GetAllRecords()
    logging.info(ret)
    if isinstance(ret, dbus.String):
        return True
    else:
        return False


@checkword
def getRecordById():
    """
    根据ID查询通知记录
    """
    id = get_id()
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    ret = property_obj.GetRecordById(id)
    logging.info(ret)
    if isinstance(ret, dbus.String):
        return True
    else:
        return False


@checkword
def show():
    """
    改变通知中心的显示状态
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    property_obj.Show()
    time.sleep(2)
    return True


@checkword
def toggle():
    """
    显示通知中心
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    property_obj.Toggle()
    time.sleep(1)
    return True


def recordCount():
    """
    获取通知中心中通知的数量
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    ret = property_obj.recordCount()
    logging.info(ret)
    return ret


@checkword
def checkRecordCountNum():
    """
    检查记录数正确
    """
    ret = recordCount()
    if ret == 1:
        return True
    else:
        return False


def getAppSetting(app):
    """
    根据app的名称获取配置
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    ret = property_obj.getAppSetting(app)
    logging.info(ret)
    return True


def setAppSetting(app):
    """
    设置应用配置
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    ret = property_obj.getAppSetting(app)
    logging.info(ret)
    return True


def enableDeviceByPath(path, mode):
    """
    通过路径打开或断开网络
    """
    property_obj = sessionCommon.session_bus(dbus_name='com.deepin.daemon.Network',
                                             dbus_path='/com/deepin/daemon/Network',
                                             iface_name='com.deepin.daemon.Network')
    if mode == 'enable':
        property_obj.EnableDevice(path, True)
    elif mode == 'disable':
        property_obj.EnableDevice(path, False)
    else:
        logging.info("传入参数有误，请检查！")

    time.sleep(8)


def get_id():
    """
    获取通知id值
    """
    clearRecords()
    enableDeviceByPath('/org/freedesktop/NetworkManager/Devices/2', 'enable')
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    ret = property_obj.GetAllRecords()
    logging.info(ret)
    ids = re.findall(r'(\d+)', ret)[0]
    logging.info(ids)
    return ids


@checkword
def closeNotification(id):
    """
    根据通知id关闭通知气泡
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    property_obj.CloseNotification(id)
    return True


@checkword
def removeRecord():
    """
    根据ID删除通知记录
    """
    id_num = get_id()
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    property_obj.RemoveRecord(id_num)
    return True


@checkword
def org_get_capabilities():
    """
    获取功能项
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.Notifications')
    ret = property_obj.GetCapabilities()
    logging.info(ret)
    if isinstance(ret, dbus.Array):
        return True
    else:
        return False


@checkword
def org_get_ServerInformation():
    """
    获取服务信息
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.Notifications')
    ret = property_obj.GetServerInformation()
    logging.info(ret)
    if isinstance(ret, tuple):
        return True
    else:
        return False


@checkword
def org_closeNotification(id):
    """
    根据通知id关闭通知气泡
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    property_obj.CloseNotification(id)
    return True


if __name__ == '__main__':
    import sys
    import time

    I_g = logging.getLogger()
    I_g.setLevel(logging.DEBUG)
    s_h = logging.StreamHandler(sys.stdout)
    I_g.addHandler(s_h)

    # getAppList()
    # getCapbilities()
    # clearRecords()
    # getServerInformation()
    # getAllRecords()
    # getRecordById('1')
    # recordCount()
    # toggle()
    # time.sleep(3)
    # hide()
    # enableDeviceByPath('/org/freedesktop/NetworkManager/Devices/2', 'enable')
    # get_id()
    # re_test()
    # getRecordById()
    # checkClearRecords()
    # removeRecord()
    org_get_ServerInformation()
