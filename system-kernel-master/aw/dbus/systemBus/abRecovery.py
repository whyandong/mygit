# -*- coding:utf-8 -*-
import os
import random
import logging

import dbus

from frame.decorator import checkword
from aw.dbus.dbus_common import get_system_dbus_interface

DBUS_NAME = 'com.deepin.ABRecovery'
DBUS_PATH = '/com/deepin/ABRecovery'
IFACE_NAME = 'com.deepin.ABRecovery'


# ===========================
#         功能函数
# ===========================
def dbus_interface():
    return get_system_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


def get_properties_value(properties: str):
    property_obj = get_system_dbus_interface(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(IFACE_NAME, properties)
    return result


def start_backup():
    """
    开始备份
    :return: None
    """
    dbus_interface().StartBackup()


def backing_up():
    """
    是否正在备份
    :return:True or False
    """
    result = get_properties_value('BackingUp')
    return bool(result)


# ===========================
#         服务方法
# ===========================
@checkword
def canBackup():
    """
    CanBackup() -> (bool can)
    能否备份
    参数
        无
    返回
        can:能否备份
    :return:True or False
    """
    result = dbus_interface().CanBackup()
    if isinstance(result, dbus.Boolean):
        logging.info(bool(result))
        return True
    else:
        logging.info(f'返回数据不是{dbus.Boolean}:{type(result)}')
        return False


@checkword
def canRestore():
    """
    CanRestore() -> (bool can)
    能否恢复
    参数
        无
    返回
        can:能否恢复
    :return:True or False
    """
    result = dbus_interface().CanRestore()
    if isinstance(result, dbus.Boolean):
        logging.info(bool(result))
        return True
    else:
        logging.info(f'返回数据不是{dbus.Boolean}:{type(result)}')
        return False


@checkword
def startBackup():
    """
    StartBackup()
    开始备份
    参数
        无
    返回
        无
    :return:True or False
    """
    dbus_interface().StartBackup()
    return True


# def StartRestore():#不开发
#     """
#     StartRestore()
#     开始恢复
#     参数
#         无
#     返回
#         无
#     :return:
#     """
#     pass


# ===========================
#         服务属性
# ===========================
@checkword
def backingUp(target=False):
    """
    bool BackingUp
    是否正在备份
    :param target: True or False
    :return:True or False
    """
    result = get_properties_value('BackingUp')
    if isinstance(result, dbus.Boolean):
        logging.info(f'target: {target}')
        logging.info(f'result: {bool(result)}')
        if bool(result) == target:
            return True
        else:
            return False
    else:
        logging.info(f'返回数据不是{dbus.Boolean}:{type(result)}')
        return False


@checkword
def restoring(target=False):
    """
    bool Restoring
    是否正在恢复
    :param target: True or False
    :return:True or False
    """
    result = get_properties_value('Restoring')
    if isinstance(result, dbus.Boolean):
        logging.info(f'target: {target}')
        logging.info(f'result: {bool(result)}')
        if bool(result) == target:
            return True
        else:
            return False
    else:
        logging.info(f'返回数据不是{dbus.Boolean}:{type(result)}')
        return False


@checkword
def configValid():
    """
    bool ConfigValid
    是否配置文件正确无误
    :return:True or False
    """
    result = get_properties_value('ConfigValid')
    if isinstance(result, dbus.Boolean):
        logging.info(bool(result))
        return True
    else:
        logging.info(f'返回数据不是{dbus.Boolean}:{type(result)}')
        return False


@checkword
def backupTime():
    """
    int64 BackupTime
    备份时间 unix 时间戳
    :return:True or False
    """
    result = get_properties_value('BackupTime')
    if isinstance(result, dbus.Int64):
        logging.info(int(result))
        return True
    else:
        logging.info(f'返回数据不是{dbus.Int64}:{type(result)}')
        return False


@checkword
def backupVersion():
    """
    string BackupVersion
    备份的系统版本
    :return:True or False
    """
    result = get_properties_value('BackupVersion')
    if isinstance(result, dbus.String):
        logging.info(str(result))
        return True
    else:
        logging.info(f'返回数据不是{dbus.String}:{type(result)}')
        return False


@checkword
def getHasBackedUp():
    """
    当前系统运行,是否完成过备份.用于控制中心判断是否需要执行备份
    :return:True or False
    """
    result = get_properties_value('HasBackedUp')
    if isinstance(result, dbus.Boolean):
        logging.info(bool(result))
        return True
    else:
        logging.info(f'返回数据不是{dbus.Boolean}:{type(result)}')
        return False


# ===========================
#         服务信号
# ===========================
@checkword
def jobEnd(dbus_monitor, parse_flg: str):
    """
    JobEnd(string kind,bool success,string errMsg)
    在备份或恢复任务结束发出。
    参数
        kind 在备份时为 "backup"，在恢复时为 "restore"。
        success 是否成功
        errMsg 失败时的错误消
    :param dbus_monitor: dbus_common.DbusMonitor类的实例,且已运行start
    :param parse_flg:检查用字符串,判断此字符串在不在返回的结果中
    :return:True or False
    """
    result = dbus_monitor.parse()
    logging.info(f'success parse_flg:\n{parse_flg}')
    logging.info(f'success result:\n{result}')
    if parse_flg in result:
        logging.info('parse_flg在result中')
        return True
    else:
        logging.info('parse_flg不在result,请检查此接口')
        return False
