# -*- coding:utf-8 -*-
import logging
import re
import time
import dbus

from aw.dbus.dbus_common import get_session_dbus_interface
from frame.decorator import checkword
from subprocess import getstatusoutput

DBUS_NAME = 'com.deepin.dde.Dock'
DBUS_PATH = '/com/deepin/dde/Dock'
IFACE_NAME = 'com.deepin.dde.Dock'


# ===========================
#         功能函数
# ===========================
def dbus_interface():
    return get_session_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)

def get_properties_value(properties: str):
    property_obj = get_session_dbus_interface(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(IFACE_NAME, properties)
    return result

def getPlugin():
    """
    获取加载的插件列表信息，转化成列表类型
    :return: list
    """
    interface = dbus_interface()
    dbus_out = interface.GetLoadedPlugins()
    logging.info(dbus_out)
    list_ = []
    for i in range(len(dbus_out)):
        t = re.findall(r'\S*', dbus_out[i])
        list_.append(t[0])
    return list_

@checkword
def getLoadedPlugins():
    """
    获取插件列表信息，判断列表信息类型是否正常
    :return: list
    """
    dbus_out = getPlugin()
    logging.info(type(dbus_out))
    if isinstance(dbus_out, list):
        logging.info("返回数据类型为list正常")
        return True
    else:
        logging.info(f'返回数据类型为list异常，当前返回值类型为{type(dbus_out)}')
        return False

@checkword
def reloadPlugins():
    """
    重新加载插件列表信息
    :return: list
    """
    interface = dbus_interface()
    dbus_out = interface.ReloadPlugins()
    logging.info(dbus_out)
    return True

@checkword
def checkreloadPlugins():
    """
    重载后，重新获取插件列表信息，数据类型是否正常
    :return: list
    """
    dbus_out = getPlugin()
    logging.info(dbus_out)
    if isinstance(dbus_out, list):
        logging.info("返回数据类型为list正常")
        return True
    else:
        logging.info(f'返回数据类型为list异常，当前返回值类型为{type(dbus_out)}')
        return False


def getPluginVisible(pluName):
    """
     获取某个插件是否可见状态
     :return: boolean
    """
    interface = dbus_interface()
    isVisible = interface.getPluginVisible(pluName)
    return isVisible

def setPluginVisible(pluName, status):
    """
     设置某个插件是否可见状态
     :return: 无
    """
    interface = dbus_interface()
    interface.setPluginVisible(pluName, status)
    return True

@checkword
def get_PluginVisible(kwList):
    """
     获取重载后插件列表中各个插件的可见状态，并与原来的插件列表状态对比，判断是否一致（部分机器的某插件状态一直false)
     :return: list
    """
    pluList = []
    for i in kwList:
        isVisible = getPluginVisible(i)
        if isVisible:
            pluList.append(i)
    list_ = set(kwList) - set(pluList)
    if len(list_) < len(kwList):
        logging.info(f'当前插件 {pluList} 在dock栏显示，部分插件{list_}没有显示')
        return True
    else:
        logging.info(f'没有插件在dock栏显示')
        return False

@checkword
def set_PluginVisible(pluname, mode):
    """
     根据不同的模式，设置某个插件可见状态，并判断状态设置生效
     :return: boolean
    """
    # status = getPluginVisible(pluname)
    # logging.info(status)
    if mode == 'visible':
        setPluginVisible(pluname, True)
        status_ = getPluginVisible(pluname)
        logging.info(status_)
        if status_:
            return True
        else:
            return False
    elif mode == 'invisible':
        setPluginVisible(pluname, False)
        status_ = getPluginVisible(pluname)
        logging.info(status_)
        if not status_:
            return True
        else:
            return False

@checkword
def resizeDock(size):
    """
     设置改变dock栏的大小
     :return: 无
    """
    time.sleep(1)
    interface = dbus_interface()
    interface.resizeDock(size, True)
    return True

@checkword
def callShow():
    """
     设置显示dock任务栏
     :return: 无
    """
    time.sleep(1)
    interface = dbus_interface()
    interface.callShow()
    return True

# ===========================
#         服务属性
# ===========================
@checkword
def geometry():
    """
    获取dock栏的位置，并进行各位置坐标值的类型判断是否正常
    struct of (Int32, Int32, Int32, Int32) geometry(read)
    :return:True or False
    """
    _ = (dbus.Int32, dbus.Int32, dbus.Int32, dbus.Int32)
    result = get_properties_value('geometry')
    logging.info(result)
    if isinstance(result, dbus.Struct):
        new_tuple = zip(result, _)
        for item in new_tuple:
            if isinstance(item[0], item[1]):
                logging.info(item[0])
            else:
                return False
        return True
    else:
        logging.info(f'返回数据类型不匹配,类型为：{type(result)}')
        return False

@checkword
def showInPrimary():
    """
    获取dock栏状态，判断是否仅在主屏显示
    Boolean showInPrimary(read/write)
    :return:True or False
    """
    # result_list = [0, 1, 2]
    result = get_properties_value('showInPrimary')
    logging.info(result)
    if isinstance(result, dbus.Boolean):
        return True
    else:
        logging.info(f'返回数据类型不匹配,类型为：{type(result)}')
        return False