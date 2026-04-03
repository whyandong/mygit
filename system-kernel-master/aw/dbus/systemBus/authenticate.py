# -*- coding: utf-8 -*-
import time
import dbus
import logging

from aw.dbus.systemBus import systemCommon
from frame.decorator import checkword
from subprocess import getstatusoutput
from aw.dbus.dbus_common import get_system_dbus_interface

dbus_name = 'com.deepin.daemon.Authenticate'
dbus_path = '/com/deepin/daemon/Authenticate'
iface_name = 'com.deepin.daemon.Authenticate'

dbpath_list = []

# ===========================
#         功能函数
# ===========================
def system_bus(dbus_name=dbus_name, dbus_path=dbus_path,
               iface_name=iface_name):
    system_bus = dbus.SystemBus()
    system_obj = system_bus.get_object(dbus_name, dbus_path)
    property_obj = dbus.Interface(system_obj, dbus_interface=iface_name)
    return property_obj


def dbus_interface():
    return get_system_dbus_interface(dbus_name, dbus_path, iface_name)


def cmd_input(passwd, dbus_name=dbus_name, dbus_path=dbus_path, dbus_iface=None):
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


def authenticate(user, flag, type):
    """
    根据flag开启不同的认证 flag: 1:密码认证，2：指纹认证，4：人脸认证
    :return: String
    """
    interface = system_bus()
    result = interface.Authenticate(user, flag, type)
    dbpath_list.append(result)
    logging.info(result)
    return result


def resetLimits(passwd, user):
    """
    开启不同flag方式的认证，校验返回数据类型
    :return:String
    """
    result = cmd_input(passwd,
                       dbus_iface='com.deepin.daemon.Authenticate.ResetLimits string:"{}"'.format(user))
    logging.info(result)


@checkword
def getSupportedFlags():
    """
    可支持的认证flag，认证接口中传入的flag必须在这个范围内
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name=dbus_name, dbus_path=dbus_path,
                                           iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Authenticate', 'SupportedFlags')
    logging.info(result)
    if isinstance(result, dbus.Int32):
        logging.info(f'获取可支持的认证flag值{result}成功')
        print(f'获取可支持的认证flag值{result}成功')
        return True
    else:
        logging.info('获取可支持的认证flag失败')
        return False


@checkword
def authenticate1(user, flag, type):
    """
    开启不同flag方式的认证，校验返回数据类型
    :return:String
    """
    result = authenticate(user, flag, type)
    if isinstance(result, dbus.String):
        logging.info('返回数据类型为dbus.Boolean正常')
        return True
    else:
        logging.info(f'返回数据类型异常,返回值类型为{type(result)}')
        return False


@checkword
def getLimits(user):
    """
    开启不同flag方式的认证，校验返回数据类型
    :return:String
    """
    interface = system_bus()
    result = interface.GetLimits(user)
    logging.info(result)
    if isinstance(result, dbus.String):
        logging.info('返回数据类型为dbus.String正常')
        return True
    else:
        logging.info(f'返回数据类型异常,返回值类型为{type(result)}')
        return False


@checkword
def checkLimits(user):
    """
    开启不同flag方式的认证，校验返回数据类型
    :return:String
    """
    interface = system_bus()
    result = interface.GetLimits(user)
    logging.info(result)
    if isinstance(result, dbus.String):
        logging.info('返回数据类型为dbus.String正常')
        return True
    else:
        logging.info(f'返回数据类型异常,返回值类型为{type(result)}')
        return False


@checkword
def preOneKeyLogin(flag):
    """
    开启不同flag方式的认证，校验返回数据类型
    :return:String
    """
    interface = system_bus()
    result = interface.PreOneKeyLogin(flag)
    logging.info(result)
    if isinstance(result, dbus.String):
        logging.info('返回数据类型为dbus.String正常')
        return True
    else:
        logging.info(f'返回数据类型异常,返回值类型为{type(result)}')
        return False


@checkword
def quit(passwd):
    """
    开启不同flag方式的认证会话，全部退出关闭
    :return: 无
    """
    for i in dbpath_list:
        result = cmd_input(passwd, dbus_path=i,
                           dbus_iface='com.deepin.daemon.Authenticate.Session.Quit')
        if result:
            logging.info(f"开启认证会话{i}关闭成功!")
            return True
        else:
            logging.info(f"开启认证会话{i}关闭失败!")
            return False
