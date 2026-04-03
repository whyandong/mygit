# -*- coding:utf-8 -*-
import logging

import dbus

from frame.decorator import checkword
from aw.dbus.dbus_common import get_system_dbus_interface

DBUS_NAME = 'com.deepin.daemon.Apps'
DBUS_PATH = '/com/deepin/daemon/Apps'
IFACE_NAME = 'com.deepin.daemon.Apps.LaunchedRecorder'


def dbus_interface():
    return get_system_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


def get_all_new_apps():
    interface = dbus_interface()
    apps_map = interface.GetNew()
    apps_list = []
    for key in apps_map:
        for desktop in apps_map[key]:
            apps_list.append(f'{key}/{desktop}.desktop')
    return apps_list


def is_new_apps(desktop_file: str, target=True) -> bool:
    """
    检查
    :param target:
    :param desktop_file:
    :return: True or False
    """
    apps_list = get_all_new_apps()
    if (desktop_file in apps_list) == target:
        return True
    else:
        return False


@checkword
def getNew() -> bool:
    """
    GetNew() -> (map[string][]string newApps),获取已经安装但从未打开使用过的应用列表
    newApps: 返回的map结构中，key表示应用的desktopFile所在目录，value表示从未打开的应用的id列表
    :return: True or False
    """
    interface = dbus_interface()
    apps_map = interface.GetNew()
    logging.info(apps_map)
    if isinstance(apps_map, dbus.Dictionary):
        for key in apps_map:
            if not isinstance(key, dbus.String):
                logging.info(f'返回数据不是{dbus.String}:{type(key)}')
                return False

            if isinstance(apps_map[key], dbus.Array):
                for desktop in apps_map[key]:
                    if isinstance(desktop, dbus.String):
                        pass
                    else:
                        logging.info(f'返回数据不是{dbus.String}:{type(desktop)}')
                        return False
            else:
                logging.info(f'返回数据不是{dbus.Array}:{type(apps_map[key])}')
                return False
    else:
        logging.info(f'返回数据不是{dbus.Dictionary}:{type(apps_map)}')
        return False

    return True


def markLaunched(desktopFile):
    """
    MarkLaunched(string desktopFile)
    标记某个应用是否启动过
    参数
        desktopFile: 标记该应用启动过，标记以后该应用的id就不会出现在GetNew函数返回的结构中
    返回
        无
    :param desktopFile:
    :return:True or False
    """
    interface = dbus_interface()
    interface.MarkLaunched(dbus.String(desktopFile))


@checkword
def uninstallHints(desktop_file):
    """
    UninstallHints(string[] desktopFile)
    删除某个程序关联的一组desktopFile的记录应用是否启动过的状态信息
    参数
        desktopFile: 某个应用的所有desktopFile文件路径
    返回
        无
    :param desktop_file:
    :return: True
    """

    desktop_file_list = [desktop_file]
    interface = dbus_interface()
    interface.UninstallHints(dbus.Array(desktop_file_list))
    return True


@checkword
def watchDirs(dir_):
    """
    WatchDirs(string[] dirs)
    增加监视的目录，监视该目录文件的删除和新增事件
    参数
        dirs: 要增加的被监视目录列表
    返回
        无
    :param dir_: 目录路径
    :return: True
    """

    dirs = [dir_]
    interface = dbus_interface()
    interface.WatchDirs(dbus.Array(dirs))
    return True


@checkword
def statusSaved(dbus_monitor, *parse_flgs: str):
    """
    StatusSaved (string, string, bool)
    标记某个应用是否启动过的状态文件被保存的信号
    第一个参数为应用的desktopFile文件目录，第二个为标记记录配置文件，第三个为是否标记成功
    :param dbus_monitor:dbus_common.DbusMonitor类的实例,且已运行start
    :param parse_flgs:检查用字符串,判断此字符串在不在返回的结果中
    :return:True or False
    """
    result = dbus_monitor.parse()
    logging.info(f'StatusSaved result:\n{result}')
    for parse_flg in parse_flgs:
        logging.info(f'StatusSaved parse_flg:\n{parse_flg}')
        if parse_flg in result:
            logging.info('parse_flg在result中')
        else:
            logging.info('parse_flg不在result,请检查此接口')
            return False
    else:
        return True
