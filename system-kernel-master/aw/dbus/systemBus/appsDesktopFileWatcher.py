# -*- coding: utf-8 -*-
import os
import random
import logging

import dbus

from frame.decorator import checkword
from frame.constant import resoure_path
from aw.dbus.dbus_common import get_system_dbus_interface

DBUS_NAME = 'com.deepin.daemon.Apps'
DBUS_PATH = '/com/deepin/daemon/Apps'
IFACE_NAME = 'com.deepin.daemon.Apps.DesktopFileWatcher'


@checkword
def event(dbus_monitor, *parse_flgs: str):
    """
    Event (string, uint32)
    服务监视的目录如果有文件新增或者删除，会触发该信号
    第一个参数为新增或者删除的文件绝对路径字符串
    第二个参数为0
    :param dbus_monitor: dbus_common.DbusMonitor类的实例,且已运行start
    :param parse_flgs:检查用字符串,判断此字符串在不在返回的结果中
    :return:True or False
    """
    result = dbus_monitor.parse()
    logging.info(f'success result:\n{result}')
    for parse_flg in parse_flgs:
        logging.info(f'ItemChanged parse_flg:\n{parse_flg}')
        if parse_flg in result:
            logging.info('parse_flg在result中')
        else:
            logging.info('parse_flg不在result,请检查此接口')
            return False
    else:
        return True
