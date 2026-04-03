# -*- coding: utf-8 -*-
import logging
import time

import dbus

from aw.dbus.dbus_common import get_system_dbus_interface
from aw.dbus.dbus_common import execute_command_by_subprocess
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.daemon.Daemon'
DBUS_PATH = '/com/deepin/daemon/Daemon'
IFACE_NAME = 'com.deepin.daemon.Daemon'


# 程序：/usr/lib/deepin-daemon/dde-system-daemon
# 功能：提供设置和获取系统配置的守护进程


def dbus_interface():
    return get_system_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


def get_scale_Ply_mouth():
    """
    获取当前开机主题
    :return: 开机主题，uos-ssd-logo or uos-hidpi-ssd-logo
    """
    ret = execute_command_by_subprocess('plymouth-set-default-theme')
    print(ret)
    return ret


@checkword
def networkGetConnections():
    """
    获取wifi连接配置信息
    :return:True or False
    """

    interface = dbus_interface()
    result = interface.NetworkGetConnections()
    print(result)
    if isinstance(result, dbus.Array):
        logging.info("返回数据类型为dbus.Array正常")
        return True
    else:
        logging.info("返回数据类型为dbus.Array异常")
        return False


def scalePlymouth(scale):
    """
    设置开机启动图形主题
    ScalePlymouth(uint32 scale) -> ()
    :param scale:设置主题选项,1或2，或其他
    :return: None
    """
    interface = dbus_interface()
    interface.ScalePlymouth(dbus.UInt32(scale))
    time.sleep(20)

@checkword
def checkScalePlymouth(scale):
    """
    检查开机启动图形主题
    :param scale: 1 or 2
    :return:True or False
    """
    ret = get_scale_Ply_mouth()
    if scale == 1:
        if 'uos-ssd-logo' in ret:
            logging.info("设置开机启动图形主题为uos-ssd-logo成功")
            return True
        else:
            logging.info("设置开机启动图形主题为uos-ssd-logo失败")
            return False
    elif scale == 2:
        if 'uos-hidpi-ssd-logo' in ret:
            logging.info("设置开机启动图形主题为uos-hidpi-ssd-logo成功")
            return True
        else:
            logging.info("设置开机启动图形主题为uos-hidpi-ssd-logo失败")
            return False
    else:
        logging.info("参数传入错误，请检查")
        return False


@checkword
def setLongPressDuration(duration):
    """
    设置手势触屏事件时间上限
    SetLongPressDuration(uint32 duration) -> ()
    :param duration:超时时间，单位毫秒，系统默认700ms
    :return:True or False
    """
    interface = dbus_interface()
    result = interface.SetLongPressDuration(dbus.UInt32(duration))
    logging.info(result)
    if not result:
        logging.info(f"设置手势触屏事件时间{duration}ms上限成功")
        return True
    else:
        logging.info(f"设置手势触屏事件时间{duration}ms上限失败")
        return False

@checkword
def clearTty(ttyid):
    """
    清除指定tty打印数据
    :param ttyid: 登录用户的tty编号
    :return: 无
    """
    interface = dbus_interface()
    interface.ClearTty(dbus.UInt32(ttyid.strip()[-1]))
    return True

@checkword
def clearTtys():
    """
    清除所有tty打印数据
    :return: 无
    """
    interface = dbus_interface()
    interface.ClearTtys()
    return True

@checkword
def isPidVirtualMachine(pids):
    """
    判断进程是否运行在虚拟机，通过各个进程号的运行结果返回类型是否正常
    ：params: UInt32 number；过滤掉首尾的脏进程数据，一般为非虚拟机进程号
    :return: Boolean
    """
    pids = pids.split("\n")
    for i in range(1, len(pids)-1):
        result = dbus_interface().IsPidVirtualMachine(dbus.UInt32(pids[i].strip()))
        if isinstance(result, dbus.Boolean):
            pass
        else:
            logging.info(f"部分进程号{pids[i]}的运行状态类型异常，返回值类型为{type(result)}")
            return False
    logging.info(f"所有进程号的运行状态类型正常，检查进程号共计{len(pids)-2}个")
    return True


if __name__ == '__main__':
    import sys

    # I_g = logging.getLogger()
    # I_g.setLevel(logging.DEBUG)
    # s_h = logging.StreamHandler(sys.stdout)
    # I_g.addHandler(s_h)

    # networkGetConnections()
    scale = 1
    scalePlymouth(scale)
    checkScalePlymouth(scale)
    setLongPressDuration(700)
