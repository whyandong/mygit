# -*- coding: utf-8 -*-
import logging

import dbus

from aw.dbus.dbus_common import get_system_dbus_interface
from aw.dbus.dbus_common import execute_command_by_subprocess
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.daemon.SwapSchedHelper'
DBUS_PATH = '/com/deepin/daemon/SwapSchedHelper'
IFACE_NAME = 'com.deepin.daemon.SwapSchedHelper'


# 功能：提供用户登录时设置DDECGroups环境的接口


def dbus_interface():
    return get_system_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


def get_sessionID():
    """
    获取sessionID
    :return: sessionID值
    """
    ret = execute_command_by_subprocess('cat /proc/self/sessionid')
    return ret


def prepare(mode):
    """
    为登录用户准备DDECGroups环境
    :param mode:valid or invalid
    :return:None
    """
    if mode == 'valid':
        sessionID = get_sessionID()
        logging.info(f'sessionID为{sessionID}')
        try:
            interface = dbus_interface()
            out = interface.Prepare(sessionID)
            return out
        except dbus.exceptions.DBusException as e:
            dbus_message = e.get_dbus_message()
            return dbus_message
    elif mode == 'invalid':
        sessionID = '1sssss'
        logging.info(f'sessionID为{sessionID}')
        try:
            interface = dbus_interface()
            out = interface.Prepare(sessionID)
            logging.info("在try中执行")
            return out
        except dbus.exceptions.DBusException as e:
            dbus_message = e.get_dbus_message()
            return dbus_message


# @checkword
def checkPrepareStatus(mode):
    """
    检查Prepare方法执行正常（jenkins 执行脚本的进程不在任何session 中，本地执行）
    :param mode:valid or invalid
    :return:True or False
    """
    ret = prepare(mode)
    logging.info(ret)
    if mode == 'valid':
        if not ret:
            logging.info('检查输入有效sessionID接口运行正常')
            return True
        else:
            logging.info('检查输入有效sessionID接口运行异常')
            return False
    elif mode == 'invalid':
        if 'not found session' in ret:
            logging.info('检查输入无效sessionID接口报错信息正确')
            return True
        else:
            logging.info('检查输入无效sessionID接口报错信息有误')
            return False
