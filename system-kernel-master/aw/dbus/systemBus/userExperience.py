# -*- coding: utf-8 -*-
import logging
import dbus
import time

from frame.decorator import checkword
from aw.dbus.systemBus import systemCommon

dbus_name = 'com.deepin.userexperience.Daemon'
dbus_path = '/com/deepin/userexperience/Daemon'
iface_name = 'com.deepin.userexperience.Daemon'


def enableUserexperience(mode):
    """
    打开或关闭用户体验计划
    :param mode:enable or disable
    :return:None
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    if mode == 'enable':
        out = property_obj.Enable(dbus.Boolean(True))
        logging.info(out)
    elif mode == 'disable':
        out = property_obj.Enable(dbus.Boolean(False))
        logging.info(out)
    else:
        logging.info("参数错误，请检查！")
    time.sleep(2)


def isEnabled():
    """
    返回用户体验计划是否开启或关闭
    :return:开关状态
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    out = property_obj.IsEnabled()
    logging.info(out)
    return out


@checkword
def checkIsEnabled():
    """
    检查返回值成功
    :return: True or False
    """
    ret = isEnabled()
    if ret == 0 or 1:
        logging.info("检查返回值成功")
        return True
    else:
        logging.info("检查返回值失败")
        return False


@checkword
def checkEnableUserexperience(type):
    """
    检查用户体验计划开关状态
    :param type: enable or disable
    :return:True or False
    """
    ret = isEnabled()
    if type == 'enable':
        if ret == 1:
            logging.info("检查用户体验计划打开成功")
            return True
        else:
            logging.info("检查用户体验计划打开失败")
            return False
    elif type == 'disable':
        if ret == 0:
            logging.info("检查用户体验计划关闭成功")
            return True
        else:
            logging.info("检查用户体验计划关闭失败")
            return False
    else:
        logging.info("参数错误，请检查！")
        return False


@checkword
def sendAppInstallData(path, name, id, mode):
    """
    向数据埋点程序发送应用的安装和卸载消息，埋点程序将这些数据上报到远端服务器
    :param path:安装或者卸载的应用程序的desktopFile路径
    :param name:安装或者卸载的应用程序名称
    :param id:安装或者卸载的应用程序id
    :param mode:installapp表示安装应用，uninstallapp表示卸载应用
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    if mode == 'install':
        out = property_obj.SendAppInstallData('installapp', path, name, id)
        logging.info(out)
        if not out:
            logging.info("向数据埋点程序发送应用的安装消息成功")
            return True
        else:
            logging.info("向数据埋点程序发送应用的安装消息失败")
            return False
    elif mode == 'uninstall':
        out = property_obj.SendAppInstallData('uninstallapp', path, name, id)
        logging.info(out)
        if not out:
            logging.info("向数据埋点程序发送应用的卸载消息成功")
            return True
        else:
            logging.info("向数据埋点程序发送应用的卸载消息失败")
            return False
    else:
        logging.info("参数错误，请检查！")
        return False


@checkword
def sendAppStateData(path, name, id, mode):
    """
    向数据埋点程序发送应用的打开和关闭消息，埋点程序将这些数据上报到远端服务器
    :param path:安装或者卸载的应用程序的desktopFile路径
    :param name:安装或者卸载的应用程序名称
    :param id:安装或者卸载的应用程序id
    :param mode:openapp表示打开应用，closeapp表示关闭应用
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    if mode == 'open':
        out = property_obj.SendAppStateData('openapp', path, name, id)
        logging.info(out)
        if not out:
            logging.info("向数据埋点程序发送应用的打开消息成功")
            return True
        else:
            logging.info("向数据埋点程序发送应用的打开消息失败")
            return False
    elif mode == 'close':
        out = property_obj.SendAppInstallData('closeapp', path, name, id)
        logging.info(out)
        if not out:
            logging.info("向数据埋点程序发送应用的关闭消息成功")
            return True
        else:
            logging.info("向数据埋点程序发送应用的关闭消息失败")
            return False
    else:
        logging.info("参数错误，请检查！")
        return False


@checkword
def sendLogonData(mode):
    """
    向数据埋点程序发送用户登录和退出登录消息
    :param mode:login表示用户登录事件，logout表示用户登出事件，shutdown表示用户关机事件
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    if mode == 'login':
        out = property_obj.SendLogonData('login')
        logging.info(out)
        if not out:
            logging.info("向数据埋点程序发送用户登录消息成功")
            return True
        else:
            logging.info("向数据埋点程序发送用户登录消息失败")
            return False
    elif mode == 'logout':
        out = property_obj.SendLogonData('logout')
        logging.info(out)
        if not out:
            logging.info("向数据埋点程序发送用户退出登录消息成功")
            return True
        else:
            logging.info("向数据埋点程序发送用户退出登录消息失败")
            return False
    elif mode == 'shutdown':
        out = property_obj.SendLogonData('shutdown')
        logging.info(out)
        if not out:
            logging.info("向数据埋点程序发送用户关机消息成功")
            return True
        else:
            logging.info("向数据埋点程序发送用户关机消息失败")
            return False
    else:
        logging.info("参数错误，请检查！")
        return False
