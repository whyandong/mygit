# -*- coding: utf-8 -*-
import re
import time
import json
import logging

import dbus

from frame.decorator import checkword
from aw.dbus.dbus_common import get_session_dbus_interface
from aw.dbus.sessionBus import dock, sessionCommon

dbus_name = 'com.deepin.SessionManager'
dbus_path = '/com/deepin/StartManager'
iface_name = 'com.deepin.StartManager'


def dbus_interface():
    return get_session_dbus_interface(dbus_name, dbus_path, iface_name)


def get_properties_value(properties: str):
    property_obj = get_session_dbus_interface(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(iface_name, properties)
    return result


def add_autostart(filename):
    """
    添加自启文件
    :param filename: 自动启动的文件名
    :return: None
    """
    try:
        interface = dbus_interface()
        interface.AddAutostart(dbus.String(filename))
        logging.info(f'添加自启动项成功，file：{filename}')
    except Exception as e:
        logging.info(f'添加自启动项失败，file：{filename}')
        logging.exception(e)


def remove_autostart(filename):
    """
    移除自启文件
    :param filename: 自动启动的文件名
    :return: None
    """
    try:
        interface = dbus_interface()
        interface.RemoveAutostart(dbus.String(filename))
        logging.info(f'移除自启动项成功，file：{filename}')
    except Exception as e:
        logging.info(f'移除自启动项失败，file：{filename}')
        logging.exception(e)


"""
=========================功能函数=================================
=========================接口方法=================================
"""


@checkword
def addAutostart(filename, err=False, err_type=1):
    """
    AddAutostart (string filename) -> (bool value),设置文件自动启动
    参数
        filename: 自动启动的文件名
    返回
        value: 自动启动设置成功返回 true， 否则为false
    :param filename: 自动启动的文件名
    :param err: 是否引发‘invalid layout’错误
    :param err_type: 错误类型,传入1、2。 主动报错类型：1、failed to get app id, 2、copy file failed
    :return: True or False
    """
    err_type_dict = {1: 'failed to get app id', 2: 'copy file failed'}

    logging.info(f"设置文件 {filename} 自动启动")
    interface = dbus_interface()
    if err:
        err_name = err_type_dict[err_type]
        try:
            logging.info(f"预期引发{err_name}错误")
            interface.AddAutostart(dbus.String(filename))
            logging.info(f"未成功引发{err_name}")
            return False
        except dbus.DBusException as e:
            if err_name in e.get_dbus_message():
                logging.info(f"成功引发{err_name}")
                return True
            else:
                logging.info(f"引发的错误与预期不符合：{err_name}")
                return False
    else:
        result = interface.AddAutostart(dbus.String(filename))
        time.sleep(0.5)
        if isinstance(result, dbus.Boolean):
            logging.info(f"添加结果: {result}")
            if bool(result) is True:
                return True
            else:
                logging.info(f"添加结果不符合预期")
                return False
        else:
            logging.info(f"AddAutostart 返回的数据类型不是预期的bus.Boolean，实际类型为{type(result)}")
            return False


@checkword
def autostartList():
    """
    AutostartList () -> ([]string value),获得自动启动的列表
    参数
        无
    返回
        value: 返回一个字符串数组的自动启动列表
    :return:
    """

    logging.info(f"获得自动启动的列表")
    interface = dbus_interface()
    result = interface.AutostartList()
    if isinstance(result, dbus.Array):
        logging.info(f"自动启动的列表: {result}")
        for item in result:
            logging.info(item)
        return True
    else:
        logging.info(f"AutostartList 返回的数据类型不是预期的bus.Array，实际类型为{type(result)}")
        return False


@checkword
def dumpMemRecord():
    """
    DumpMemRecord () -> (string value),获取记录的应用程序进程内存占用信息。
    参数
        无
    返回
        value: 返回备份的字符串
    :return:
    """
    logging.info(f"获取记录的应用程序进程内存占用信息")
    interface = dbus_interface()
    result = interface.DumpMemRecord()
    if isinstance(result, dbus.String):
        logging.info(f"应用程序进程内存占用信息: {result}")
        mminfo = json.loads(result)
        for key in mminfo:
            logging.info(f'{key}: {mminfo[key]}')
        return True
    else:
        logging.info(f"DumpMemRecord 返回的数据类型不是预期的bus.String，实际类型为{type(result)}")
        return False


@checkword
def getApps():
    """
    GetApps () -> (map[uint32]string value),得到App的序列号描述表
    参数
        无
    返回
        value: 返回序列号为键和描述为值的map
    :return:
    """
    logging.info(f"获取App的序列号描述表")
    interface = dbus_interface()
    result = interface.GetApps()
    if isinstance(result, dbus.Dictionary):
        logging.info(f"App序列号描述表: {result}")
        keys = sorted(result.keys())
        for key in keys:
            logging.info(f'{key}: {result[key]}')
        return True
    else:
        logging.info(f"GetApps 返回的数据类型不是预期的bus.Dictionary，实际类型为{type(result)}")
        return False


@checkword
def isAutostart(filename, target=True):
    """
    IsAutostart (string filename) -> (bool value),判断文件是否已经加入自动启动中
    参数
         filename: 要判断的文件名
    返回
         value: 已经加入返回true, 否则为false
    :return:
    """
    logging.info(f"判断文件{filename}是否已经加入自动启动中")
    interface = dbus_interface()
    result = interface.IsAutostart(dbus.String(filename))
    if isinstance(result, dbus.Boolean):
        logging.info(f"{filename}是否已经加入自动启动中: {result}")
        logging.info(f'target: {target}')
        if bool(result) == target:
            logging.info(f'符合预期结果')
            return True
        else:
            return False
    else:
        logging.info(f"IsAutostart 返回的数据类型不是预期的bus.Boolean，实际类型为{type(result)}")
        return False


@checkword
def isMemSufficient():
    """
    IsMemSufficient () -> (bool value),检查内存是否充足
    参数
        无
    返回
        value: 充足返回true，否则返回false
    :return:
    """
    logging.info(f"检查内存是否充足")
    interface = dbus_interface()
    result = interface.IsMemSufficient()
    logging.info(f'result: {result}')
    if isinstance(result, dbus.Boolean):
        logging.info(f"检查内存是否充足: {bool(result)}")
        return True
    else:
        logging.info(f"IsMemSufficient 返回的数据类型不是预期的bus.Boolean，实际类型为{type(result)}")
        return False



@checkword
def launch(desktopfile):
    """
    Launch (string desktopfile) -> (bool value),启动桌面App
    参数
        desktopfile: 桌面App的名字
    返回
        value: 成功启动返回true， 否则为false
    :param desktopfile: 桌面App的名字
    :return:
    """
    logging.info(f"启动桌面App")
    interface = dbus_interface()
    result = interface.Launch(desktopfile)
    if isinstance(result, dbus.Boolean):
        logging.info(f"是否启动成功: {result}")
        return True
    else:
        logging.info(f"Launch 返回的数据类型不是预期的bus.Boolean，实际类型为{type(result)}")
        return False

def close_app():
    """
    调用close_window方法关闭文件管理器
    """
    dock.closeWindow()

def LaunchApp():
    """
    LaunchApp (string desktopfile, uint32 timestamp, string[] file) -> (),启动桌面App, 带有时间戳记录
    参数
        desktopfile: 桌面文件名
        timestamp: 时间戳
        file： 文件路径名
    返回
        无
    :return:
    """
    pass


def LanchAppAction():
    """
    LaunchAppAction (string desktopfile, string action, uint32 timestamp) -> (),以特定的功能启动App
    参数
        desktopfile: 桌面文件名
        action: 特定启动方式名
        timestamp: 时间戳
    返回
        无
    :return:
    """
    pass


def LaunchAppWithOptions():
    """
    LaunchAppWithOptions (string desktopfile, uint32 timestamp, []string files, map[string]dbus.Variant options) -> ()
    启动App，并设置Key Path信息
    参数
        desktopfile: 桌面文件名
        timestamp: 时间戳
        files: 文件路径名
        options: 包含名字和dbus变量的表
    返回
        无
    :return:
    """
    pass


def LaunchWithTimestamp():
    """
    LaunchWithTimestamp (string desktopfile, uint32 timestamp) -> (bool value),带有时间戳记录的启动
    参数
        desktopfile: 桌面文件名
        timestamp: 时间戳
    返回
        value: 启动成功返回true
    :return:
    """
    pass


def RemoveAutostart():
    """
    RemoveAutostart (string filename) ↦ (bool value),将文件移出自动启动
    参数
        filename: 文件名
    返回
        value: 移除成功返回true，否则返回false
    :return:
    """
    pass


def RunCommand():
    """
    RunCommand (string exe, []string arg) -> (),执行命令
    参数
        exe: 执行的可执行文件
        arg: 传入exe的参数
    返回
        无
    :return:
    """
    pass


def RunCommandWithOptions():
    """
    RunCommandWithOptions (string exe, []string arg, map[string]dbus.Variant option) -> ()
    根据option字典获得dir，指定命令执行的目录
    参数
        exe: 执行的可执行文件
        arg: 传入exe的参数
        option: 包含名字和dbus变量的表
    返回
        无
    :return:
    """
    pass


def TryAgain():
    """
    TryAgain (bool launch) -> (),再次尝试启动因为内存不足而未启动的对象
    参数
        launch: true 表示需要尝试启动， false则不进行启动，仅打印信息
    返回
        无
    :return:
    """
    pass


"""
=========================接口方法=================================
=========================接口属性=================================
"""



@checkword
def getNeededMemory():
    """
    SessionManager 设置属性状态的值
    :return:Int32
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.StartManager', 'NeededMemory')
    logging.info(f'接口返回的最大值为{result}')
    if isinstance(result, dbus.UInt64):
        logging.info("获取SessionStartManager需要的内存大小值成功")
        return True
    else:
        logging.info(f"获取的内存大小值失败不是预期的Uint64,获取到的值的类型为{type(result)}")
        return False




"""
=========================接口方法=================================
=========================接口信号=================================
"""


def AutostartChanged():
    """
    AutostartChanged(string status, string name),发送加入或移除自动启动队列文件的信息
    :return:
    """
    pass
