# -*- coding: utf-8 -*-
import time
import dbus
import logging

from frame.decorator import checkword
from aw.common import excute_cmd
from aw.dbus.dbus_common import get_system_dbus_interface
from subprocess import getstatusoutput

DBUS_NAME = 'com.deepin.defender.risantiav'
DBUS_PATH = '/com/deepin/defender/risantiav'
IFACE_NAME = 'com.deepin.defender.risantiav'


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
def startApp():
    """
    开启服务,需要时间完成，否则可能会影响其它信息的获取或设置
    :return: 无
    """
    dbus_interface().StartApp()
    # if sec:
    #     time.sleep(sec)
    time.sleep(1)
    return True


@checkword
def exitApp():
    """
    退出服务,需要时间完成
    :return: 无
    """
    dbus_interface().ExitApp()
    # if sec:
    #     time.sleep(sec)
    time.sleep(1)
    return True


@checkword
def checkApp(appName, mode):
    """
    开启或退出服务后,校验相关服务进程是否存在
    :return: 无
    """
    cmd = f"ps -ef | grep {appName} | grep -v grep"
    out = excute_cmd(cmd)
    logging.info(out)
    if mode == 'start':
        if out:
            logging.info(f"{mode}服务，获取进程名{appName}存在，检验正常")
            return True
        else:
            logging.info(f"{mode}服务，获取进程名{appName}不存在，检验异常")
            return False
    elif mode == 'exit':
        if not out:
            logging.info(f"{mode}服务，获取进程名{appName}不存在，检验正常")
            return True
        else:
            logging.info(f"{mode}服务，获取进程名{appName}存在，检验异常")
            return False


@checkword
def getRisingLocalVersion():
    """
    得到瑞星本地版本号
    :return: 无
    """
    dbus_interface().GetRisingLocalVersion()
    return True


@checkword
def getRisingSrvVersion():
    """
    得到瑞星服务器版本号
    :return: 无
    """
    dbus_interface().GetRisingSrvVersion()
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
def updateVersion():
    """
    更新病毒库
    :return: 无
    """
    dbus_interface().UpdateVersion()
    return True


@checkword
def setScanFileSize(size):
    """
    设置允许扫描文件大小
    :return: 无
    """
    dbus_interface().SetScanFileSize(size)
    return True


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
