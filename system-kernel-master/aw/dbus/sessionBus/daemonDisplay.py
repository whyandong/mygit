# -*- coding: utf-8 -*-
import re
import time
import json
import logging

import dbus

from frame.decorator import checkword
from aw.dbus.dbus_common import get_session_dbus_interface

dbus_name = 'com.deepin.SessionManager'
dbus_path = '/com/deepin/daemon/Display'
iface_name = 'com.deepin.daemon.Display'


def dbus_interface():
    return get_session_dbus_interface(dbus_name, dbus_path, iface_name)


def get_properties_value(properties: str):
    property_obj = get_session_dbus_interface(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(iface_name, properties)
    return result


def get_Brightness():
    """
    获改变显示器亮度,只有带实体亮度调节按键的机器可以传False
    :return: Dict
    """

    interface = dbus_interface()
    result = interface.GetBrightness()
    if isinstance(result, dbus.Dictionary):
        logging.info(f'获取显示器名称和亮度值的的值为{result}')
        return result
    else:
        logging.info(f"属性的值不是预期的Dict,实际类型为{type(result)}")
        return False


def get_Monitors():
    """
    获取当前显示器的对象列表（连接状态的）
    :return:Array Objec Path
    """
    result = get_properties_value('Monitors')
    logging.info(result)
    if isinstance(result, dbus.Array):
        logging.info(f"获取显示的路径成功,路径{result}")
        return result[0]
    else:
        logging.info(f"获取显示器的路径失败,获取到的值为{result}")
        return False

def get_Brightness():
    """
    获改变显示器亮度,只有带实体亮度调节按键的机器可以传False
    :return: Dict
    """

    interface = dbus_interface()
    result = interface.GetBrightness()

    if isinstance(result, dbus.Dictionary):
        logging.info(f'获取显示器名称值为{result}')
        return result
    else:
        logging.info(f"属性的值不是预期的Dict,实际类型为{type(result)}")
        return False

def get_listOutputNames():
    """
    列出所有显示器的名称
    :param:
    :return: Byte
    """
    interface = dbus_interface()
    result = interface.ListOutputNames()
    if isinstance(result, dbus.Array):
        logging.info(f'获取显示器名称的值为{result[0]}')
        return result[0]
    else:
        logging.info(f"获取显示器名称的值不是预期的Array,实际类型为{type(result)}")
        return False
"""
=========================功能函数=================================
=========================接口方法=================================
"""


@checkword
def applyChanges():
    """
    应用设置更改
    :return:
    """
    interface = dbus_interface()
    interface.ApplyChanges()
    logging.info(f'应用设置更改成功')
    return True


@checkword
def associateTouch(outputname, touchserial):
    """
    将触控和显示触控设备名映射
    :param:outputname:显示器名称
    param:touchserial:触控设备序列号
    :return:
    """

    interface = dbus_interface()
    interface.AssociateTouch(dbus.String(outputname), dbus.String(touchserial))

    logging.info(f'将触控和显示触控设备名映射成功')
    return True


@checkword
def canRotate():
    """
    判断是否能旋转屏幕
    :return: Boolean
    """

    interface = dbus_interface()
    result = interface.CanRotate()
    if isinstance(result, dbus.Boolean):
        logging.info(f'是否能旋转屏幕的值为{result}')
        return True
    else:
        logging.info(f"是否能旋转屏幕的值不是预期的Boolean，实际类型为{type(result)}")
        return False


@checkword
def canSetBrightness(outputname):
    """
    判断显示屏幕是否支持设置亮度
    :param:outputname:显示器名称 String
    :return: Boolean
    """

    interface = dbus_interface()
    result = interface.CanSetBrightness(dbus.String(outputname))
    if isinstance(result, dbus.Boolean):
        logging.info(f'是否支持设置亮度的值为{result}')
        return True
    else:
        logging.info(f"是否支持设置亮度的值不是预期的Boolean，实际类型为{type(result)}")
        return False


@checkword
def changeBrightness(raised):
    """
    判断显示屏幕是否支持设置亮度
    :param:raised: True or False Boolean
    :return:
    """

    interface = dbus_interface()
    interface.ChangeBrightness(dbus.Boolean(raised))
    logging.info(f'传入亮度的值为{raised}')
    return True


@checkword
def getBrightness():
    """
    获改变显示器亮度,只有带实体亮度调节按键的机器可以传False
    :return: Dict
    """

    interface = dbus_interface()
    result = interface.GetBrightness()
    if isinstance(result, dbus.Dictionary):
        logging.info(f'获取显示器名称和亮度值的的值为{result}')
        return True
    else:
        logging.info(f"属性的值不是预期的Dict,实际类型为{type(result)}")
        return False


@checkword
def deleteCustomMode(name):
    """
    删除自定义模式
    :param: name String 自定义模式的名称
    :return:
    """

    interface = dbus_interface()
    interface.DeleteCustomMode(dbus.String(name))
    logging.info(f'删除自定义模式成功')
    return True


@checkword
def getBrightness():
    """
    获取显示器名称和亮度值的字典
    :param:
    :return: Dict
    """
    interface = dbus_interface()
    result = interface.GetBrightness()
    if isinstance(result, dbus.Dictionary):
        logging.info(f'获取显示器名称和亮度值的字典的值为{result}')
        return True
    else:
        logging.info(f"属性的值不是预期的Dict,实际类型为{type(result)}")
        return False


@checkword
def getBuiltinMonitor():
    """
    获得内建显示器信息，就是电脑自带的显示器
    :param:
    :return: Dict
    """
    interface = dbus_interface()
    result = interface.GetBuiltinMonitor()
    if isinstance(result[0], dbus.String):
        logging.info(f'获取显示器名称和path值的字典的值为{result[0]}')
        return True
    else:
        logging.info(f"属性的值不是预期的String,实际类型为{type(result)}")
        return False


@checkword
def getRealDisplayMode():
    """
    获得真实的显示模式，有如下模式：
    Custom 0 自定义
    Mirror 1 镜像
    Extend 2 扩展
    OnlyOne 3 只开启一个
    Unknow 4 未知

    :param:
    :return: Byte
    """
    interface = dbus_interface()
    result = interface.GetRealDisplayMode()
    if isinstance(result, dbus.Byte):
        logging.info(f'获取显示模式的值为{result}')
        return True
    else:
        logging.info(f"获取显示模式的值不是预期的Byte,实际类型为{type(result)}")
        return False


@checkword
def listOutputNames():
    """
    列出所有显示器的名称
    :param:
    :return: Byte
    """
    interface = dbus_interface()
    result = interface.ListOutputNames()
    if isinstance(result, dbus.Array):
        logging.info(f'获取显示器名称的值为{result}')
        return True
    else:
        logging.info(f"获取显示器名称的值不是预期的Array,实际类型为{type(result)}")
        return False


@checkword
def listOutputsCommonModes():
    """
    列出通用显示模式的信息
    :param:
    :return: Byte
    """
    interface = dbus_interface()
    result = interface.ListOutputsCommonModes()
    if isinstance(result, dbus.Array):
        logging.info(f'获取通用显示模式的值为{result}')
        return True
    else:
        logging.info(f"获取通用显示模式的值不是预期的Array,实际类型为{type(result)}")
        return False


@checkword
def modifyConfigName(name, newname):
    """
    更改自定义设置的名称
    :param:name 要更改的显示设备名称 String
    :param:newname 更改的显示设备新名称 String
    :return:
    """
    interface = dbus_interface()
    interface.ModifyConfigName(dbus.String(name), dbus.String(newname))
    logging.info(f'已将原显示器名称{name}更改为新名称{newname}')
    return True


@checkword
def refreshBrightness():
    """
    更改自定义设置的名称
    :param:重设屏幕亮度，使用记录的亮度值设置一次亮度，用于 session 切换时把亮度修改为刚切换到的那个 session 的亮度
    :return:
    """
    interface = dbus_interface()
    interface.RefreshBrightness()
    logging.info(f'重设屏幕亮度成功')
    return True


@checkword
def resetChanges():
    """
    重置设置，还原之前的修改。
    :param:
    :return:
    """
    interface = dbus_interface()
    interface.ResetChanges()
    logging.info(f'重置设置，还原之前的修改成功')
    return True


@checkword
def save():
    """
    保存显示模式设置
    :param:
    :return:
    """
    interface = dbus_interface()
    result = interface.Save()
    logging.info(f'保存显示模式设置成功')
    return True


@checkword
def setAndSaveBrightness(outputname, tmp_value):
    """
    更改自定义设置的名称
    :param:outputname 显示设备名称 String
    :param:tmp_vlaue 显示设备亮度属性值 Double
    :return:
    """
    interface = dbus_interface()

    interface.SetAndSaveBrightness(dbus.String(outputname), dbus.Double(tmp_value))
    logging.info(f'已将原显示器名称{outputname}亮度属性值更改为{tmp_value}')

    logging.info(f"调用getBrightness(),获取显示设备亮度信息")
    test_value = get_Brightness()
    if test_value == {dbus.String(outputname): dbus.Double(tmp_value)}:
        logging.info(f'设置字显示设备亮度信息成功')
        return True
    else:
        logging.info(f'设置字显示设备亮度信息设置失败,设置的亮度值为{tmp_value}，生效的亮度为{test_value}')
        return True


@checkword
def setBrightness(outputname, tmp_value):
    """
    更改自定义设置的名称
    :param:outputname 显示设备名称 String
    :param:tmp_vlaue 显示设备亮度属性值 Double
    :return:
    """
    interface = dbus_interface()

    interface.SetBrightness(dbus.String(outputname), dbus.Double(tmp_value))
    logging.info(f'已将原显示器名称{outputname}亮度属性值更改为{tmp_value}')

    logging.info(f"调用get_Brightness(),获取显示设备亮度信息")
    test_value = get_Brightness()
    if test_value == {dbus.String(outputname): dbus.Double(tmp_value)}:
        logging.info(f'设置字显示设备亮度信息成功')
        return True
    else:
        logging.info(f'设置字显示设备亮度信息设置失败,设置的亮度值为{tmp_value}，生效的亮度为{test_value}')
        return True


@checkword
def setColorTemperature(color_tmp):
    """
    设置色温
    :param:color_tmp 设置色温 Int32
    :return:
    """
    interface = dbus_interface()
    logging.info(f"调用setColorTemperature(),设置色温为{color_tmp}")
    interface.SetColorTemperature(dbus.Int32(color_tmp))

    logging.info(f"调用get_properties_value(),获色温")
    test_value = get_properties_value('ColorTemperatureManual')

    if test_value == dbus.Int32(color_tmp):
        logging.info(f'设置色温成功')
        return True
    else:
        logging.info(f'设置色温的调节模式信息失败,设置色温的调节模式值为{color_tmp}，生效的色温的调节模式为{test_value}')
        return True


@checkword
def setMethodAdjustCCT(adjustMethod):
    """
    设置色温的调节模式
    adjustMethod: 色温的调节模式， 0 不调节色温， 1 自动调节， 2 手动调节。其他情况抛出错误
    :param:tmp_vlaue 显示设备亮度属性值 Double
    :return:
    """
    interface = dbus_interface()
    logging.info(f"调用setMethodAdjustCCT(),设置色温的调节模式更改为{adjustMethod}")
    interface.SetMethodAdjustCCT(dbus.Int32(adjustMethod))

    logging.info(f"调用get_properties_value(),获色温的调节模式")
    test_value = get_properties_value('ColorTemperatureMode')

    if test_value == dbus.Int32(adjustMethod):
        logging.info(f'设置色温的调节模式成功')
        return True
    else:
        logging.info(f'设置色温的调节模式信息失败,设置色温的调节模式值为{adjustMethod}，生效的色温的调节模式为{test_value}')
        return True


@checkword
def switchMode(mode, name):
    """
    切换显示的模式
    :param:mode 显示模式 Byte
    :param:name 在 mode 为 Custom 0 时，此为自定义模式的名称；在 mode 为 OnlyOne 3 时，此为显示器的名称；其他情况下此值无意义。
    显示模式可选值如下：
    Custom 0 自定义
    Mirror 1 镜像
    Extend 2 扩展
    OnlyOne 3 只开启一个
    :return:
    """
    interface = dbus_interface()

    interface.SwitchMode(dbus.Byte(mode), dbus.String(name))
    logging.info(f'已将原显示器名称{mode}亮度属性值更改为{name}')
    logging.info(f'设置字显示设备亮度信息成功')
    return True


'''==============================属性方法========================================'''


@checkword
def getMonitors():
    """
    获取当前显示器的对象列表（连接状态的）
    :return:Array Objec Path
    """
    result = get_properties_value('Monitors')
    logging.info(result)
    if isinstance(result, dbus.Array):
        logging.info("获取显示器的对象列表成功")
        return True
    else:
        logging.info(f"获取显示器的对象列表失败,获取到的值为{result}")
        return False


@checkword
def getCustomIdList():
    """
    获取自定义配置的Id列表
    :return:Array Objec Path
    """
    result = get_properties_value('CustomIdList')
    logging.info(result)
    if isinstance(result, dbus.Array):
        logging.info("获取显自定义配置的Id列表成功")
        return True
    else:
        logging.info(f"获取自定义配置的Id列表失败,获取到的值为{result}")
        return False


@checkword
def getTouchscreens():
    """
    获取触摸屏的信息
            id： 标识符
            name： 名称
            deviceNode： 设备节点，其实是内核设备文件
            serial： 序列号
    :return:int32 id
            string name
            string deviceNode
            string serial

    """
    result = get_properties_value('Touchscreens')
    logging.info(result)
    if isinstance(result, dbus.Array):
        logging.info("获取触摸屏的信息成功")
        return True
    else:
        logging.info(f"获取触摸屏的信息失败,获取到的值为{result}")
        return False


@checkword
def getHasChanged():
    """
    获取是否修改了显示设置但未保存

    :return:Boolean

    """
    result = get_properties_value('HasChanged')
    logging.info(result)
    if isinstance(result, dbus.Boolean):
        logging.info("获取是否修改了显示设置但未保存信息成功")
        return True
    else:
        logging.info(f"获取是否修改了显示设置但未保存的信息失败,获取到的值为{result}")
        return False


@checkword
def getDisplayMode():
    """
    获取显示模式:显示模式可选值如下：

        Custom 0 自定义
        Mirror 1 镜像
        Extend 2 扩展
        OnlyOne 3 只开启一个

    :return:Byte

    """
    result = get_properties_value('DisplayMode')
    logging.info(result)
    if isinstance(result, dbus.Byte):
        logging.info("获取显示模式信息成功")
        return True
    else:
        logging.info(f"获取显示模式的信息失败,获取到的值为{result}")
        return False


@checkword
def getBrightness():
    """
    获取显示器名称和亮度的字典
    :return:Dict

    """
    result = get_properties_value('Brightness')
    logging.info(result)
    if isinstance(result, dbus.Dictionary):
        logging.info("获取显示器名称和亮度的字典成功")
        return True
    else:
        logging.info(f"获取显示器名称和亮度的字典信息失败,获取到的值为{result}")
        return False


@checkword
def getTouchMap():
    """
    获取触控设备到显示器的映射,键为触控设备序列号，值为显示器名称
    :return:Dict

    """
    result = get_properties_value('TouchMap')
    logging.info(result)
    if isinstance(result, dbus.Dictionary):
        logging.info("获取触控设备到显示器的映射成功")
        return True
    else:
        logging.info(f"获触控设备到显示器的映射信息失败,获取到的值为{result}")
        return False


@checkword
def getColorTemperatureManual():
    """
    获取色温调节模式为手动时的色温值
    :return:Int32

    """
    result = get_properties_value('ColorTemperatureManual')
    logging.info(result)
    if isinstance(result, dbus.Int32):
        logging.info("获取色温调节模式为手动时的色温值成功")
        return True
    else:
        logging.info(f"获取色温调节模式为手动时的色温值信息失败,获取到的值为{result}")
        return False


@checkword
def getColorTemperatureMode():
    """
    获取色温调节模式
    :return:Int32

    """
    result = get_properties_value('ColorTemperatureMode')
    logging.info(result)
    if isinstance(result, dbus.Int32):
        logging.info("获取色温调节模式值成功")
        return True
    else:
        logging.info(f"获取色温调节模式值信息失败,获取到的值为{result}")
        return False


@checkword
def getCurrentCustomId():
    """
    获取当前自定义显示模式的 id
    :return:String

    """
    result = get_properties_value('CurrentCustomId')
    logging.info(result)
    if isinstance(result, dbus.String):
        logging.info("获取当前自定义显示模式的 id值成功")
        return True
    else:
        logging.info(f"获取当前自定义显示模式的 id值信息失败,获取到的值为{result}")
        return False


@checkword
def getPrimary():
    """
    获取主显示器的名称
    :return:String

    """
    result = get_properties_value('Primary')
    logging.info(result)
    if isinstance(result, dbus.String):
        logging.info("获取主显示器的名称值成功")
        return True
    else:
        logging.info(f"获取当前主显示器的名称信息失败,获取到的值为{result}")
        return False


@checkword
def getPrimaryRect():
    """
    获取主显示器的位置区域
    :return:String

    """
    result = get_properties_value('PrimaryRect')
    logging.info(result)
    if isinstance(result, dbus.Struct):
        logging.info("获取主显示器的位置区域成功")
        return True
    else:
        logging.info(f"获取主显示器的位置区域信息失败,获取到的值为{result}")
        return False


@checkword
def getScreenHeight():
    """
    获取屏幕的高度
    :return:Uint16

    """
    result = get_properties_value('ScreenHeight')
    logging.info(result)
    if isinstance(result, dbus.UInt16):
        logging.info("获取获取屏幕的高度")
        return True
    else:
        logging.info(f"获取获取屏幕的高度信息失败,获取到的值为{result}")
        return False


@checkword
def getScreenWidth():
    """
    获取屏幕的宽度，屏幕 Screen 指能放下所有显示器矩形的大矩形
    :return:Uint16

    """
    result = get_properties_value('ScreenWidth')
    logging.info(result)
    if isinstance(result, dbus.UInt16):
        logging.info("获取获取屏幕的宽度")
        return True
    else:
        logging.info(f"获取获取屏幕的宽度信息失败,获取到的值为{result}")
        return False


@checkword
def getMaxBacklightBrightness():
    """
    获取屏幕背光亮度最大值，所有背光控制器的亮度允许最大值。用于告知前端（控制中心）是否让调节亮度的滑块控件显示刻度线，如果数值较小才显示
    :return:Uint32

    """
    result = get_properties_value('MaxBacklightBrightness')
    logging.info(f'接口返回的最大值为{result}')
    if isinstance(result, dbus.UInt32):
        logging.info("获取屏幕背光亮度最大值")
        return True
    else:
        logging.info(f"获取屏幕背光亮度最大值信息失败,获取到的值的类型为{type(result)}")
        return False
