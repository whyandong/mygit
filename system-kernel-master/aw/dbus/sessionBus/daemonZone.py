# -*- coding: utf-8 -*-
import logging

import dbus

from aw.dbus.dbus_common import get_session_dbus_interface
from frame.decorator import checkword
from aw.dbus.sessionBus import sessionCommon

DBUS_NAME = 'com.deepin.daemon.Zone'
DBUS_PATH = '/com/deepin/daemon/Zone'
IFACE_NAME = 'com.deepin.daemon.Zone'


def dbus_interface():
    return get_session_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


def get_properties_value(properties: str):
    property_obj = get_session_dbus_interface(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(IFACE_NAME, properties)
    return result


def set_properties_value(properties: str, value):
    property_obj = get_session_dbus_interface(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    property_obj.Set(IFACE_NAME, properties, value)


@checkword
def setBottomLeft(value):
    """
    设置左下角动作
    :param: value String
    :return:True or False
    """
    interface = dbus_interface()
    interface.SetBottomLeft(value)
    return True


@checkword
def setBottomRight(value):
    """
    设置右下角动作
    :param: value String
    :return:True or False
    """
    interface = dbus_interface()
    interface.SetBottomRight(value)
    return True


@checkword
def setTopLeft(value):
    """
    设置左上角动作
    :param: value String
    :return:True or False
    """
    interface = dbus_interface()
    interface.SetTopLeft(value)
    return True


@checkword
def setTopRight(value):
    """
    设置右上角动作
    :param: value String
    :return:True or False
    """
    interface = dbus_interface()
    interface.SetTopRight(value)
    return True


@checkword
def topLeftAction():
    """
    获取左上角动作
    :return:True or False
    """
    interface = dbus_interface()
    result = interface.TopLeftAction()
    logging.info(result)
    if isinstance(result, dbus.String):
        return True
    else:
        logging.info(f'返回类型错误，返回数据类型为{type(result)}')
        return False


@checkword
def topRightAction():
    """
    获取右上角动作
    :param: value String
    :return:True or False
    """
    interface = dbus_interface()
    result = interface.TopRightAction()
    logging.info(result)
    if isinstance(result, dbus.String):
        return True
    else:
        logging.info(f'返回类型错误，返回数据类型为{type(result)}')
        return False


@checkword
def bottomLeftAction():
    """
    获取左下角动作
    :return:True or False
    """
    interface = dbus_interface()
    result = interface.BottomLeftAction()
    logging.info(result)
    if isinstance(result, dbus.String):
        return True
    else:
        logging.info(f'返回类型错误，返回数据类型为{type(result)}')
        return False


@checkword
def bottomRightAction():
    """
    获取右下角动作
    :param: value String
    :return:True or False
    """
    interface = dbus_interface()
    result = interface.BottomRightAction()
    logging.info(result)
    if isinstance(result, dbus.String):
        return True
    else:
        logging.info(f'返回类型错误，返回数据类型为{type(result)}')
        return False


# =================================检查函数================================
@checkword
def checkBottomLeftAction(value):
    """
    检查左下角动作是否设置成功
    :param: value String
    :return:True or False
    """

    result = get_bottomLeftAction()
    if result == value:
        return True
    else:
        logging.info(f'返回类型错误，左下角动作设置失败，返回数据类型为{type(result)}')
        return False


@checkword
def checkBottomRightAction(value):
    """
    检查右下角动作是否设置成功
    :param: value String
    :return:True or False
    """

    result = get_bottomRightAction()
    if result == value:
        return True
    else:
        logging.info(f'返回类型错误，右下角动作设置失败，返回数据类型为{type(result)}')
        return False


@checkword
def checkTopLeftAction(value):
    """
    检查左上角动作是否设置成功
    :param: value String
    :return:True or False
    """

    result = get_topLeftAction()
    if result == value:
        return True
    else:
        logging.info(f'返回类型错误，左上角动作设置失败，返回数据类型为{type(result)}')
        return False


@checkword
def checkTopRightAction(value):
    """
    检查右上角动作是否设置成功
    :param: value String
    :return:True or False
    """

    result = get_topRightAction()
    if result == value:
        return True
    else:
        logging.info(f'返回类型错误，右上角动作设置失败，返回数据类型为{type(result)}')
        return False


# ====================================属性方法==========================

def get_bottomLeftAction():
    """
    获取左下角动作
    :return:String
    """
    interface = dbus_interface()
    result = interface.BottomLeftAction()
    logging.info(result)
    if isinstance(result, dbus.String):
        return result
    else:
        logging.info(f'返回类型错误，返回数据类型为{type(result)}')
        return False


def get_bottomRightAction():
    """
    获取右下角动作
    :return:String
    """
    interface = dbus_interface()
    result = interface.BottomRightAction()
    logging.info(result)
    if isinstance(result, dbus.String):
        return result
    else:
        logging.info(f'返回类型错误，返回数据类型为{type(result)}')
        return False


def get_topLeftAction():
    """
    获取左上角动作
    :return:String
    """
    interface = dbus_interface()
    result = interface.TopLeftAction()
    logging.info(result)
    if isinstance(result, dbus.String):
        return result
    else:
        logging.info(f'返回类型错误，返回数据类型为{type(result)}')
        return False


def get_topRightAction():
    """
    获取右上角动作
    :param: value String
    :return:String
    """
    interface = dbus_interface()
    result = interface.TopRightAction()
    logging.info(result)
    if isinstance(result, dbus.String):
        return result
    else:
        logging.info(f'返回类型错误，返回数据类型为{type(result)}')
        return False


@checkword
def getmethod():
    """
    获取配置config
    """
    property_obj = sessionCommon.session_bus(dbus_name='com.deepin.daemon.Zone', dbus_path='/com/deepin/daemon/Zone',
                                             iface_name='com.deepin.sync.Config')
    result = property_obj.Get()
    logging.info(type(result))
    print(result)
    if isinstance(result, dbus.Array):
        return True
    else:
        logging.info(f'返回类型错误，返回数据类型为{type(result)}')
        return False


@checkword
def setmethod():
    """
    设置config
    """
    property_obj = sessionCommon.session_bus(dbus_name='com.deepin.daemon.Zone', dbus_path='/com/deepin/daemon/Zone',
                                             iface_name='com.deepin.sync.Config')
    result = property_obj.Get()
    property_obj.Set(result)
    return True


if __name__ == '__main__':
    # getmethod()
    setmethod()
