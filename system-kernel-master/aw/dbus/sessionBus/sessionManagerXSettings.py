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
dbus_path = '/com/deepin/XSettings'
iface_name = 'com.deepin.XSettings'


def dbus_interface():
    return get_session_dbus_interface(dbus_name, dbus_path, iface_name)


def get_properties_value(properties: str):
    property_obj = get_session_dbus_interface(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(iface_name, properties)
    return result


def get_color(prop):
    """
    输入属性里颜色相关的字段，获得字段的rgba值(红，绿，蓝，透明度的混合颜色值) 属性字段可用ListProps()获得
    :prop: 属性里颜色相关的字段 "Qt/ActiveColor"
    :return: rgba: 字段的rgba值uint16 rgba
    """

    interface = dbus_interface()
    result = interface.GetColor(dbus.String(prop))
    if isinstance(result, dbus.Array):
        logging.info(f'颜色{prop}属性字段的值为{result}')
        return result
    else:
        logging.info(f"GetColor返回的数据类型不是预期的array，实际类型为{type(result)}")
        raise ValueError(f"GetColor返回的数据类型不是预期的array，实际类型为{type(result)}")


def get_integer(prop):
    """
    输入属性里数值相关的字段，获得字段的整数数值相关的信息,属性字段可用ListProps()获得
    :prop: 属性里颜色相关的字段,"Xft/Antialias"
    :return: int32
    """

    interface = dbus_interface()
    result = interface.GetInteger(dbus.String(prop))
    if isinstance(result, dbus.Int32):
        logging.info(f'颜色{prop}属性字段的值为{result}')
        return result
    else:
        logging.info(f"GetInteger返回的数据类型不是预期的Int32，实际类型为{type(result)}")
        raise ValueError(f"GetInteger返回的数据类型不是预期的Int32，实际类型为{type(result)}")


def get_scale_factor():
    """
    获得scale-factor值，即缩放比例的值
    :return: Double
    """

    interface = dbus_interface()
    result = interface.GetScaleFactor()
    if isinstance(result, dbus.Double):
        logging.info(f'缩放比例的值为{result}')
        return True
    else:
        logging.info(f"缩放比例的值不是预期的Double，实际类型为{type(result)}")
        raise ValueError(f"缩放比例的值不是预期的Double，实际类型为{type(result)}")


def get_screen_scale_factors():
    """
    获得显示缩放比例的键值
    :return: map[string]float64/Dict
    """

    interface = dbus_interface()
    result = interface.GetScreenScaleFactors()
    if isinstance(result, dbus.Dictionary):
        logging.info(f'显示缩放比例的值为{result}')
        return result
    else:
        logging.info(f"显示缩放比例的值不是预期的Dict，实际类型为{type(result)}")
        raise ValueError(f"缩放比例的值不是预期的Double，实际类型为{type(result)}")


def get_string(prop):
    """
    获得输入属性里字符串相关的信息,属性字段可用ListProps()获得
    :param: prop string
    :return: string
    """

    interface = dbus_interface()
    result = interface.GetString(dbus.String(prop))
    if isinstance(result, dbus.String):
        logging.info(f'传入的字符串对应的值为{result}')
        return result
    else:
        logging.info(f"传入的字符串对应的值不是预期的String,实际类型为{type(result)}")
        raise ValueError(f"传入的字符串对应的值不是预期的String,实际类型为{type(result)}")


"""
=========================功能函数=================================
=========================接口方法=================================
"""


@checkword
def getColor(prop):
    """
    输入属性里颜色相关的字段，获得字段的rgba值(红，绿，蓝，透明度的混合颜色值) 属性字段可用ListProps()获得
    :prop: 属性里颜色相关的字段 "Qt/ActiveColor"
    :return: rgba: 字段的rgba值uint16 rgba
    """

    interface = dbus_interface()
    result = interface.GetColor(dbus.String(prop))
    if isinstance(result, dbus.Array):
        logging.info(f'颜色{prop}属性字段的值为{result}')
        return True
    else:
        logging.info(f"GetColor返回的数据类型不是预期的array，实际类型为{type(result)}")
        return False


@checkword
def getInteger(prop):
    """
    输入属性里数值相关的字段，获得字段的整数数值相关的信息,属性字段可用ListProps()获得
    :prop: 属性里颜色相关的字段,"Xft/Antialias"
    :return: int32
    """

    interface = dbus_interface()
    result = interface.GetInteger(dbus.String(prop))
    if isinstance(result, dbus.Int32):
        logging.info(f'颜色{prop}属性字段的值为{result}')
        return True
    else:
        logging.info(f"GetInteger返回的数据类型不是预期的Int32，实际类型为{type(result)}")
        return False


@checkword
def getScaleFactor():
    """
    获得scale-factor值，即缩放比例的值
    :return: Double
    """

    interface = dbus_interface()
    result = interface.GetScaleFactor()
    if isinstance(result, dbus.Double):
        logging.info(f'缩放比例的值为{result}')
        return True
    else:
        logging.info(f"缩放比例的值不是预期的Double，实际类型为{type(result)}")
        return False


@checkword
def getScreenScaleFactors():
    """
    获得显示缩放比例的键值
    :return: map[string]float64/Dict
    """

    interface = dbus_interface()
    result = interface.GetScreenScaleFactors()
    if isinstance(result, dbus.Dictionary):
        logging.info(f'显示缩放比例的值为{result}')
        return True
    else:
        logging.info(f"显示缩放比例的值不是预期的Dict，实际类型为{type(result)}")
        return False


@checkword
def getString(prop):
    """
    获得输入属性里字符串相关的信息,属性字段可用ListProps()获得
    :param: prop string
    :return: string
    """

    interface = dbus_interface()
    result = interface.GetString(dbus.String(prop))
    if isinstance(result, dbus.String):
        logging.info(f'传入的字符串对应的值为{result}')
        return True
    else:
        logging.info(f"传入的字符串对应的值不是预期的String,实际类型为{type(result)}")
        return False


@checkword
def listProps():
    """
    获得所有的属性字段
    :param:
    :return: string
    """

    interface = dbus_interface()
    result = interface.ListProps()
    if isinstance(result, dbus.String):
        logging.info(f'属性的值为{result}')
        return True
    else:
        logging.info(f"属性的值不是预期的String,实际类型为{type(result)}")
        return False


@checkword
def needRestartOSD():
    """
    获得输入属性里字符串相关的信息
    :param:
    :return: string
    """
    interface = dbus_interface()
    result = interface.NeedRestartOSD()
    if isinstance(result, dbus.Boolean):
        logging.info(f'属性的值为{result}')
        return True
    else:
        logging.info(f"属性的值不是预期的Boolean,实际类型为{type(result)}")
        return False


@checkword
def setColor(prop, tmp_color):
    """
    设置属性字段里颜色值
    :param:prop:属性字段
    :param:tmp_color:rgba值
    :return:
    """
    interface = dbus_interface()

    logging.info(f"调用SetColor(),设置字段颜色值为{tmp_color}")
    color = dbus.Array()
    for item in tmp_color:
        if isinstance(item, dbus.UInt16):
            color.append(item)
        else:
            color.append(dbus.UInt16(item))

    interface.SetColor(dbus.String(prop), color)
    time.sleep(5)

    logging.info(f"调用GetColor(),获取字段颜色值")
    test_color = get_color(prop)

    if color == test_color:
        logging.info(f'设置字段颜色值成功')
        return True
    else:
        logging.info(f'设置字段颜色值失败,设置的值为{tmp_color},生效的值为{test_color}')
        return False


@checkword
def setInteger(prop, tmp_value):
    """
    设置属性字段里颜色值
    :param:prop:属性字段
    :param:tmp_value:属性值
    :return:
    """
    interface = dbus_interface()

    logging.info(f"调用SetInteger(),设置字段属性值为{tmp_value}")
    interface.SetInteger(dbus.String(prop), dbus.UInt32(tmp_value))

    logging.info(f"调调用GetInteger(),获取段属性值")
    test_value = get_integer(prop)

    if dbus.UInt32(tmp_value) == test_value:
        logging.info(f'设置字段属性值成功')
        return True
    else:
        logging.info(f'设置字段属性值失败,设置的属性值为{tmp_value},生效属性值为{test_value}')
        return False


@checkword
def setScaleFactor(tmp_value):
    """
    设置属性字段里颜色值
    :param:tmp_value:缩放比
    :return:
    """
    interface = dbus_interface()

    logging.info(f"调用SetScaleFactor(),设置缩放比属性值为{tmp_value}")
    interface.SetScaleFactor(dbus.Double(tmp_value))

    logging.info(f"调用GetScaleFactor(),获取缩放比值")
    test_value = get_scale_factor()

    if dbus.Double(tmp_value) == test_value:
        logging.info(f'设置字段缩放比值成功')
        return True
    else:
        logging.info(f'设置字段属性值失败,设置的缩放比值为{tmp_value},生效属缩放比为{test_value}')
        return False


@checkword
def setScreenScaleFactors(tmp_value):
    """
    设置属性字段里颜色值
    :param:tmp_value:显示设备信息
    :return:
    """
    interface = dbus_interface()

    logging.info(f"调用SetScreenScaleFactors(),设置显示设备信息属性值为{tmp_value}")
    interface.SetScreenScaleFactors(dbus.Dictionary(tmp_value))

    logging.info(f"调用GetScreenScaleFactors(),获取显示设备信息")
    test_value = get_screen_scale_factors()

    if dbus.Dictionary(tmp_value) == test_value:
        logging.info(f'设置字显示设备信息')
        return True
    else:
        logging.info(f'设置显示设备值失败,设置的显示设备信息值为{tmp_value},生效显示设备信息为{test_value}')
        return False


@checkword
def setString(prop, tmp_value):
    """
    设置属性字段里颜色值
    :param:prop:属性字段
    :param:tmp_value:属性值
    :return:
    """
    interface = dbus_interface()

    logging.info(f"调用SetString(),设置字段属性值为{tmp_value}")
    interface.SetString(dbus.String(prop), dbus.String(tmp_value))

    logging.info(f"调调用GetString(),获取字段颜色值")
    test_value = get_string(prop)

    if dbus.String(tmp_value) == test_value:
        logging.info(f'设置字段属性值成功')
        return True
    else:
        logging.info(f'设置字段属性值失败,设置的属性值为{tmp_value},生效属性值为{test_value}')
        return False
