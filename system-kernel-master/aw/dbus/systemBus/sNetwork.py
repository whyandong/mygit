# -*- coding: utf-8 -*-
import re
import os
import socket
import time
import logging
import threading

import dbus
import netifaces

from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop

DBusGMainLoop(set_as_default=True)

from frame import constant
from aw.dbus.systemBus import systemCommon
from aw.dbus.sessionBus import dNetwork
from frame.decorator import checkword

dbus_name = 'com.deepin.system.Network'
dbus_path = '/com/deepin/system/Network'
iface_name = 'com.deepin.system.Network'


def enableDeviceByPath(path, mode):
    """
    通过路径打开或断开网络
    :param path:
    :param mode:当前接口只支持disable，enable未生效，迁移至com.deepin.daemon.Network::EnableDevice
    :return:None
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    if mode == 'enable':
        property_obj.EnableDevice(path, True)
    elif mode == 'disable':
        property_obj.EnableDevice(path, False)
    else:
        logging.info("传入参数有误，请检查！")


def isDeviceEnabled(path):
    """
    判断一个网络设备是否启用
    :param path:设备路径:/org/freedesktop/NetworkManager/Devices/2
    :return:dbus.Boolean
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    dbus_out = property_obj.IsDeviceEnabled(path)
    logging.info(dbus_out)
    time.sleep(1)
    return dbus_out


@checkword
def getIsDeviceEnabledByPath(path):
    """
    判断一个网络设备是否启用,并检查
    :return:True or False
    """
    ret = isDeviceEnabled(path)
    if ret == 0 or ret == 1:
        logging.info("判断一个网络设备启用状态成功")
        return True
    else:
        logging.info("判断一个网络设备启用状态失败")
        return False


@checkword
def checkEnableDeviceStatusByPath(path, mode):
    """
    检查网络状态是否正常
    :param path:网络路径
    :param mode:enable or disable
    :return:True or False
    """
    ret = isDeviceEnabled(path)
    if mode == 'enable':
        if ret:
            logging.info("检查打开一个网络连接成功")
            return True
        else:
            logging.info("检查打开一个网络连接失败")
            return False
    elif mode == 'disable':
        if not ret:
            logging.info("检查断开一个网络连接成功")
            return True
        else:
            logging.info("检查断开一个网络连接失败")
            return False


def ping(ip):
    """
    ping一个远程主机
    :return:string
    """
    try:
        property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
        dbus_out = property_obj.Ping(ip)
        return dbus_out
    except dbus.exceptions.DBusException as e:
        return str(e)


@checkword
def checkPingStatus(ip, mode):
    """
    检查正常IP地址内容输出
    :param ip:ip地址
    :param mode:normal or error or invalid
    :return:True or False
    """
    dbus_out = ping(ip)
    logging.info(dbus_out)
    if mode == 'normal':
        if dbus_out == None:
            logging.info("检查正常IP地址内容输出正常")
            return True
        else:
            logging.info(f"检查正常IP地址内容输出失败,返回值为{dbus_out}")
            return False
    elif mode == 'error':
        if 'no such host' in dbus_out:
            logging.info("检查错误IP地址内容输出正常")
            return True
        else:
            logging.info(f"检查错误IP地址内容输出异常,返回值为{dbus_out}")
            return False
    elif mode == 'invalid':
        if 'i/o timeout' in dbus_out:
            logging.info("检查无效IP地址内容输出正常")
            return True
        else:
            logging.info(f"检查无效IP地址内容输出异常,返回值为{dbus_out}")
            return False
    else:
        logging.info("传入参数错误，请检查")
        return False


@checkword
def getVpnEnableStatus():
    """
    获取vpn功能是否启用
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.system.Network', 'VpnEnabled')
    logging.info(dbus_out)
    if dbus_out == 0 or dbus_out == 1:
        logging.info("获取vpn功能状态成功")
        return True
    else:
        logging.info("获取vpn功能状态成功")
        return False


def toggleWirelessEnabled():
    """
    切换无线网络状态
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    dbus_out = property_obj.ToggleWirelessEnabled()
    logging.info(dbus_out)


def send_signal(devPath, mode):
    """
    设置GRUB引导菜单的背景文件的绝对路径（触发信号）
    :param devPath:
    :param mode: enable or disable
    :return:None
    """
    logging.info("开始发送触发信号")
    if mode == 'enable':
        logging.info("开始启用网络")
        dNetwork.enableDevice(devPath, 'enable')
    elif mode == 'disable':
        logging.info("开始禁用网络")
        dNetwork.enableDevice(devPath, 'disable')
    else:
        logging.info("参数错误，请检查！")


def signal_handler(*args, **kwargs):
    dbus_path0 = constant.dbus_path
    kwarg = str(kwargs)
    cmd = 'echo ' + kwarg + '>> {}/network_signal.log'.format(dbus_path0)
    os.system(cmd)


def receive_signal():
    """
    接收信号
    :return:None
    """
    logging.info("启动监护线程，接收signal信号")
    bus = dbus.SystemBus()
    bus.add_signal_receiver(signal_handler, bus_name='com.deepin.system.Network', member_keyword='member')
    loop = GLib.MainLoop()
    loop.run()


@checkword
def check_signal():
    """
    检查信号接收状态
    :return: True or False
    """
    logging.info("开始检查接收信号内容是否正确")
    dbus_path0 = constant.dbus_path
    my_file = '{}/network_signal.log'.format(dbus_path0)
    loop = 10
    while loop:
        time.sleep(2)
        if os.path.exists(my_file):
            logging.info("收集信号完成")
            with open(my_file) as f:
                content = f.readlines()
            list_ = []
            for i in content:
                pattern = r'DeviceEnabled'
                t = re.findall(pattern, i)
                if t:
                    list_.append(t[0])
            logging.info("收集到的信号内容为：{}".format(list_))
            if 'DeviceEnabled' in list_:
                logging.info("检查接收信号成功")
                return True
            else:
                logging.info("检查接收信号失败")
                return False
        else:
            logging.info("收集信号还没完成,继续等待")
            loop = loop - 1
    else:
        logging.info("等待超时，请重新收集")
        return False


def enableDevSignalRec(devPath):
    """
    启用用网络，检查信号接收
    :return:None
    """
    dbus_path0 = constant.dbus_path
    my_file = '{}/network_signal_signal.log'.format(dbus_path0)
    if os.path.exists(my_file):
        os.remove(my_file)
        logging.info("删除已存在network_signal.log文件")

    threads = []
    my_thread1 = threading.Thread(target=receive_signal)
    threads.append(my_thread1)

    my_thread2 = threading.Thread(target=send_signal, args=(devPath, 'enable'))
    threads.append(my_thread2)

    my_thread1.setDaemon(True)

    for i in threads:
        i.start()
    time.sleep(5)
    check_signal()
    if os.path.exists(my_file):
        os.remove(my_file)
        logging.info("删除已存在network_signal.log文件")
    logging.info("主线程结束")


def disableDevSignalRec(devPath):
    """
    禁用网络，检查信号接收
    :return:None
    """
    dbus_path0 = constant.dbus_path
    my_file = '{}/network_signal_signal.log'.format(dbus_path0)
    if os.path.exists(my_file):
        os.remove(my_file)
        logging.info("删除已存在network_signal.log文件")

    threads = []
    my_thread1 = threading.Thread(target=receive_signal)
    threads.append(my_thread1)

    my_thread2 = threading.Thread(target=send_signal, args=(devPath, 'disable'))
    threads.append(my_thread2)

    my_thread1.setDaemon(True)

    for i in threads:
        i.start()
    time.sleep(5)
    check_signal()
    if os.path.exists(my_file):
        os.remove(my_file)
        logging.info("删除已存在network_signal.log文件")
    logging.info("主线程结束")


def get_host_ip():
    """
    查询本机ip地址
    :return: <str> ip address
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def getGateway():
    """
    获取本机网关地址
    :return:<str> ip
    """
    routingGateway = netifaces.gateways()['default'][netifaces.AF_INET][0]
    return routingGateway

if __name__ == '__main__':
    print(get_host_ip())
