# -*- coding: utf-8 -*-
# com.deepin.dde.controlcenter相关
import os
import time
import logging

import dbus

from aw.dbus.dbus_common import get_session_dbus_interface
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.defender.daemonservice'
DBUS_PATH = '/com/deepin/defender/daemonservice'
IFACE_NAME = 'com.deepin.defender.daemonservice'


# ===========================
#         功能函数
# ===========================
def dbus_interface():
    return get_session_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


def get_properties_value(properties: str):
    property_obj = get_session_dbus_interface(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(IFACE_NAME, properties)
    return result


@checkword
def startApp():
    """
    defender启动心跳服务
    :param 无
    :return:Boolearn
    """
    interface = dbus_interface()
    interface.StartApp()
    return True


@checkword
def exitApp():
    """
    defender退出心跳服务
    :param 无
    :return:Boolearn
    """

    interface = dbus_interface()
    interface.ExitApp()
    return True


@checkword
def exitAllService():
    """
    defender退出安全中心所有服务
    :param 无
    :return:Boolearn
    """
    interface = dbus_interface()
    interface.ExitAllService()
    return True


@checkword
def exitAnalysisService():
    """
    defender退出安全中心分析服务
    :param 无
    :return:Boolearn
    """
    interface = dbus_interface()
    interface.ExitAnalysisService()
    return True


@checkword
def exitAutoStartService():
    """
    defender退出安全中心自动启动服务
    :param 无
    :return:Boolearn
    """
    interface = dbus_interface()
    interface.ExitAutoStartService()
    return True


@checkword
def exitNetControlService():
    """
    defender退出安全中心网络控制服务
    :param 无
    :return:Boolearn
    """
    interface = dbus_interface()
    interface.ExitNetControlService()
    return True


@checkword
def exitTrafficDetailService():
    """
    defender退出安全中心流量日志服务
    :param 无
    :return:Boolearn
    """
    interface = dbus_interface()
    interface.ExitTrafficDetailService()
    return True


@checkword
def exitMonitorNetFloService():
    """
    defender退出安全中心流量监控服务
    :param 无
    :return:Boolearn
    """
    interface = dbus_interface()
    interface.ExitMonitorNetFloService()
    return True


@checkword
def notifySendPassword(passwd):
    """
    defender获取系统更新数据
    :param passwd 密码
    :return:Boolearn
    """
    interface = dbus_interface()
    result = interface.notifySendPassword(passwd)
    if isinstance(result, dbus.String):
        logging.info(f'获取系统更新数据等级为{result}')
        return True
    else:
        logging.info(f"获取系统更新数据等级失败，返回的数据类型为{type(result)}")
        return False


@checkword
def getPwdLen():
    """
    defender获取密码最大长度
    :param 无
    :return:Boolean
    """
    interface = dbus_interface()
    result = interface.GetPwdLen()
    if isinstance(result, dbus.Int32):
        logging.info(f'获取到的密码最大长度为{result}')
        return True
    else:
        logging.info(f"获取最大长度失败，返回的数据类型为{type(result)}")
        return False


@checkword
def getPwdTypeLen():
    """
    defender获取密码最大长度类型
    :param 无
    :return:Boolearn
    """
    interface = dbus_interface()
    result = interface.GetPwdTypeLen()
    if isinstance(result, dbus.Int32):
        logging.info(f'获取到的密码最大长度类型为{result}')
        return True
    else:
        logging.info(f"获取最大长度失败，返回的数据类型为{type(result)}")
        return False


@checkword
def getPwdError():
    """
    defender获取密码修改错误提示文字
    :param 无
    :return:Boolearn
    """
    interface = dbus_interface()
    result = interface.GetPwdError()
    if isinstance(result, dbus.String):
        logging.info(f'获取密码修改错误提示文字为{result}')
        return True
    else:
        logging.info(f"获取密码修改错误提示文字失败，返回的数据类型为{type(result)}")
        return False


@checkword
def getPwdLimitLevel():
    """
    defender获取密码安全等级
    :param 无
    :return:Boolearn
    """
    interface = dbus_interface()
    result = interface.GetPwdLimitLevel()
    if isinstance(result, dbus.Int32):
        logging.info(f'获取密码安全等级为{result}')
        return True
    else:
        logging.info(f"获取密码安全等级失败，返回的数据类型为{type(result)}")
        return False


@checkword
def getScanStatus():
    """
    defender获取扫描状态
    :param 无
    :return:Boolearn
    """
    interface = dbus_interface()
    result = interface.GetScanStatus()
    if isinstance(result, dbus.Int32):
        logging.info(f'获取安全中心扫描状态为{result}')
        return True
    else:
        logging.info(f"获取安全中心扫描状态失败，返回的数据类型为{type(result)}")
        return False


@checkword
def setGesttingMaturityDay(value):
    """
    defender设置gsettings日期
    :param 无
    :return:Boolearn
    """
    time.sleep(1)
    interface = dbus_interface()
    interface.SetGesttingMaturityDay(dbus.Int32(value))
    return True


@checkword
def setGsetting(value):
    """
    defender设置gsettings
    :param 无
    :return:Boolearn
    """
    interface = dbus_interface()
    interface.SetGsetting(value)
    return True


@checkword
def passwordUpdate():
    """
    defender更新密码
    :param 无
    :return:Boolearn
    """
    interface = dbus_interface()
    interface.PasswordUpdate()
    return True


@checkword
def jumpScreenSecurity():
    """
    defender 屏幕安全
    :param 无
    :return:Boolearn
    """
    interface = dbus_interface()
    interface.JumpScreenSecurity()
    return True


@checkword
def jumpUpdatePolicy():
    """
    defender 屏幕安全策略
    :param 无
    :return:Boolearn
    """
    interface = dbus_interface()
    interface.JumpUpdatePolicy()
    return True


@checkword
def getSystemUpdate():
    """
    defender获取系统更新数据
    :param 无
    :return:Boolearn
    """
    interface = dbus_interface()
    result = interface.GetSystemUpdate()
    if isinstance(result, dbus.Int32):
        logging.info(f'获取系统更新数据等级为{result}')
        return True
    else:
        logging.info(f"获取系统更新数据等级失败，返回的数据类型为{type(result)}")
        return False


@checkword
def check_MaturityDay(value):
    reslut = get_MaturityDay()
    logging.info(reslut)
    if reslut == value:
        return True
    else:
        logging.info(f'获取到的值{reslut}与设置值{value}不配，检查失败')


'================属性方法==================='


@checkword
def getScanningUsbPaths():
    """
    获取usb路径信息
    """
    result = get_properties_value(dbus.String('ScanningUsbPaths'))
    logging.info(result)
    if isinstance(result, dbus.Array):
        return True
    else:
        logging.info(f'返回类型错误，返回数据类型为{type(result)}')
        return False


@checkword
def getMaturityDay():
    """
    获取gsettings到期时间
    """
    result = get_properties_value(dbus.String('MaturityDay'))
    logging.info(result)
    if isinstance(result, dbus.Int32):
        return True
    else:
        logging.info(f'返回类型错误，返回数据类型为{type(result)}')
        return False


def get_MaturityDay():
    """
    获取gsettings到期时间值
    """
    result = get_properties_value(dbus.String('MaturityDay'))
    logging.info(result)
    if isinstance(result, dbus.Int32):
        return result
    else:
        logging.info(f'返回类型错误，返回数据类型为{type(result)}')
        return False


@checkword
def getSafetygrade():
    """
    获取安全等级
    """
    result = get_properties_value(dbus.String('Safetygrade'))
    logging.info(result)
    if isinstance(result, dbus.Int32):
        return True
    else:
        logging.info(f'返回类型错误，返回数据类型为{type(result)}')
        return False

# if __name__ == '__main__':
#     # stop('network:"VPN"')
