# -*- coding: utf-8 -*-
import time
import dbus
import logging

from frame.decorator import checkword
from aw.common import excute_cmd
from aw.dbus.dbus_common import get_system_dbus_interface
from subprocess import getstatusoutput

DBUS_NAME = 'com.deepin.defender.antiav'
DBUS_PATH = '/com/deepin/defender/antiav'
IFACE_NAME = 'com.deepin.defender.antiav'


# ===========================
#         功能函数
# ===========================
def system_bus(dbus_name=DBUS_NAME, dbus_path=DBUS_PATH,
               iface_name=IFACE_NAME):
    system_bus = dbus.SystemBus()
    system_obj = system_bus.get_object(dbus_name, dbus_path)
    property_obj = dbus.Interface(system_obj, dbus_interface=iface_name)
    return property_obj


def dbus_interface():
    return get_system_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


def getScanStatus():
    """
    得到病毒查杀扫描状态：0：未开始，1：扫描中，3：扫描完成不正常， 4:扫描完成正常
    :return: Int32 status
    """
    status = dbus_interface().GetScanStatus()
    logging.info(status)
    return status


def cmd_input(passwd, dbus_name=DBUS_NAME, dbus_path=DBUS_PATH, dbus_iface=None):
    # cmd = 'sudo dbus-send --system --print-reply  --dest={} {} {}'.format(dbus_name, dbus_path, dbus_iface)
    cmd = f'echo {passwd} | sudo -S dbus-send --system --print-reply  --dest={dbus_name} {dbus_path} {dbus_iface}'
    time.sleep(1)
    logging.info(cmd)
    (status, output) = getstatusoutput(cmd)
    logging.info(output)
    if status == 0:
        logging.info(f'命令执行成功{status}')
        return output
    else:
        logging.info(f'命令执行失败{status}')
        return status


@checkword
def updateVersion():
    """
    更新病毒库
    :return: 无
    """
    dbus_interface().UpdateVersion()
    return True


@checkword
def queryVersion():
    """
    查询病毒库版本号
    :return: 无
    """
    version = dbus_interface().QueryVersion()
    logging.info(version)
    return True


@checkword
def getVdbVersion():
    """
    获取vdb本地版本号
    :return: 无
    """
    version = dbus_interface().getVdbVersion()
    logging.info(version)
    if isinstance(version, dbus.String):
        logging.info("获取病毒vdb版本号类型正常，数据类型为dbus.String正常")
        return True
    else:
        logging.info(f"获取病毒vdb版本号类型异常，返回值类型为{type(version)}")
        return False


@checkword
def isScanning():
    status = dbus_interface().isScanning()
    logging.info(status)
    if isinstance(status, dbus.Boolean):
        logging.info("获取病毒查杀扫描状态正常，数据类型为dbus.Boolean正常")
        return True
    else:
        logging.info(f"获取病毒查杀扫描状态类型异常，返回值类型为{type(status)}")
        return False


@checkword
def isTrueScanning():
    status = dbus_interface().isTrueScanning()
    logging.info(status)
    if isinstance(status, dbus.Boolean):
        logging.info("获取病毒查杀扫描状态正常，数据类型为dbus.Boolean正常")
        return True
    else:
        logging.info(f"获取病毒查杀扫描状态类型异常，返回值类型为{type(status)}")
        return False


@checkword
def backgroundUpdate():
    """
    后台更新病毒库
    :return: 无
    """
    result = dbus_interface().backgroundUpdate()
    logging.info(result)
    return True


@checkword
def scanThreatsFile():
    """
    扫描威胁文件
    :return: 无
    """
    result = dbus_interface().scanThreatsFile()
    logging.info(result)
    return True


@checkword
def setScanStart():
    """
    扫描威胁文件
    :return: 无
    """
    result = dbus_interface().setScanStart()
    logging.info(result)
    return True


@checkword
def get_ScanStatus():
    """
    得到病毒查杀扫描状态：0：未开始，1：扫描中；3：扫描完成
    :return: Int32 status
    """
    status = getScanStatus()
    logging.info(status)
    if isinstance(status, dbus.Int32):
        logging.info("获取病毒查杀扫描状态正常，数据类型为dbus.Int32正常")
        return True
    else:
        logging.info(f"获取病毒查杀扫描状态类型异常，返回值类型为{type(status)}")
        return False


@checkword
def setScanStatus(status):
    """
    设置病毒查杀扫描状态, 可自定义随机状态值
    :params: status Int32
    :return: 无
    """
    dbus_interface().SetScanStatus(status)
    return True


@checkword
def checkScanStatus(status):
    """
    得到病毒查杀扫描状态：0：未开始，1：扫描中；3：扫描完成
    :return: Int32 status
    """
    status_ = getScanStatus()
    logging.info(status)
    if isinstance(status_, dbus.Int32) and status_ == status:
        logging.info("获取病毒查杀扫描状态正常，数据类型为dbus.Int32正常")
        return True
    else:
        logging.info(f"获取病毒查杀扫描状态类型异常，返回值类型为{type(status)}")
        return False


@checkword
def queryTrustFiles():
    """
    查询信任文件
    :return: 无
    """
    dbus_interface().QueryTrustFiles()
    return True


@checkword
def queryIsolationFiles():
    """
    查询隔离文件
    :return: 无
    """
    dbus_interface().QueryIsolationFiles()
    return True


@checkword
def selectTrustAreaSize():
    """
    查询信任区文件数量
    :return: 无
    """
    result = dbus_interface().SelectTrustAreaSize()
    print(result)
    return True


@checkword
def selectIsolationAreaSize():
    """
    查询隔离区文件数量
    :return: 无
    """
    result = dbus_interface().SelectIsolationAreaSize()
    print(result)
    return True
