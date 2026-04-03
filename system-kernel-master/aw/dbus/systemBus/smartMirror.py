# -*- coding: utf-8 -*-
import logging

from frame.decorator import checkword
from aw.dbus.systemBus import systemCommon

dbus_name = 'com.deepin.lastore.Smartmirror'
dbus_path = '/com/deepin/lastore/Smartmirror'
iface_name = 'com.deepin.lastore.Smartmirror'


def setEnable(type):
    """
    设置是否使能智能选择镜像
    :param type:enable or disable
    :return:None
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    if type == 'enable':
        out = property_obj.SetEnable(True)
        logging.info(out)
    elif type == 'disable':
        out = property_obj.SetEnable(False)
        logging.info(out)
    else:
        logging.info("参数错误，请检查！")


def enable():
    """
    是否使能标志
    :return:bool
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    out = property_obj.Get('com.deepin.lastore.Smartmirror', 'Enable')
    logging.info(out)
    return out


@checkword
def getEnableStatus():
    """
    检查获取使能标志是否成功
    :return:True or False
    """
    ret = enable()
    if ret == 1 or ret == 0:
        logging.info('获取使能标志成功')
        return True
    else:
        logging.info('获取使能标志失败')
        return False


@checkword
def checkSmartmirrorStatus(mode):
    """
    检查设置使能标志是否成功
    :param mode:
    :return:True or False
    """
    ret = enable()
    if mode == 'enable':
        if ret == 1:
            logging.info('检查标志为打开成功')
            return True
        else:
            logging.info('检查标志为打开失败')
            return False
    elif mode == 'disable':
        if not ret:
            logging.info('检查标志为关闭成功')
            return True
        else:
            logging.info('检查标志为关闭失败')
            return False
    else:
        logging.info('参数错误，请检查！')
        return False


@checkword
def queryMirror(origin, official, mirror):
    """
    查询最佳镜像来源
    :param origin:'http://pools.uniontech.com/uos/pool/main/n/netselect/netselect_0.3.ds2-1+deepin_amd64.deb'
    :param official:'http://packages.chinauos.cn/uos/ '
    :param mirror:'http://cdn.packages.deepin.com/deepin/ '
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    out = property_obj.Query(origin, official, mirror)
    logging.info(out)
    if out:
        logging.info("查询最佳镜像来源成功")
        return True
    else:
        logging.info("查询最佳镜像来源失败")
        return False