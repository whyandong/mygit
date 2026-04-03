# -*- coding:utf-8 -*-
import logging

import dbus

from frame.decorator import checkword
from aw.dbus.dbus_common import get_system_dbus_interface

DBUS_NAME = 'com.deepin.daemon.Authority'
DBUS_PATH = '/com/deepin/daemon/Authority'
IFACE_NAME = 'com.deepin.daemon.Authority'


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


@checkword
def get_all_new_apps():
    interface = dbus_interface()
    apps_map = interface.GetNew()
    apps_list = []
    for key in apps_map:
        for desktop in apps_map[key]:
            apps_list.append(f'{key}/{desktop}.desktop')
    return apps_list


@checkword
def hasCookie(user):
    """
    获取当前用户的Cookie状态，校验数据类型
    :return:Boolean
    """
    interface = system_bus()
    result = interface.HasCookie(user)
    logging.info(result)
    if isinstance(result, dbus.Boolean):
        logging.info('返回用户cookie数据类型为dbus.Boolean正常')
        return True
    else:
        logging.info(f'返回用户cookie数据类型异常,返回值类型为{type(result)}')
        return False


@checkword
def checkCookie(user, cookie):
    """
    获取当前用户的Cookie状态和token，校验数据类型和状态是否有效
    :return: (Boolean result, String authToken)
    """
    interface = system_bus()
    result, token = interface.CheckCookie(user, cookie)
    logging.info(result)
    logging.info(token)
    if isinstance(result, dbus.Boolean) and isinstance(token, dbus.String):
        logging.info('返回用户cookie和token数据类型为dbus.Boolean正常')
        return True
    else:
        logging.info(f'返回用户cookie和token数据类型异常,返回值类型为{type(result)}, {type(token)}')
        return False


@checkword
def start(type, user):
    """
    开启不同flag方式的认证会话，全部退出关闭
    :return: 无 password active fingerprint face usb iris custom
    """
    path = '/home/wang1'
    interface = dbus_interface()
    result = interface.Start(type, user.strip(), path)
    print("--------",result)
    # result = cmd_input(passwd, dbus_path=i,
    #           dbus_iface='com.deepin.daemon.Authenticate.Session.Start')
    if result:
        logging.info(f"开启认证会话{i}关闭成功!")
        return True
    else:
        logging.info(f"开启认证会话{i}关闭失败!")
        return False
