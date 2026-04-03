# -*- coding: utf-8 -*-
import os
import time
import logging

import dbus

from frame.decorator import checkword
from aw.dbus.systemBus import systemCommon

dbus_name = 'com.deepin.system.Power'
dbus_path = '/com/deepin/system/Power'
iface_name = 'com.deepin.system.Power'


@checkword
def lockCpuFreq(governor,locktime):
    """
    设置CPU的高效模式运行时间
    param:governor String cpu模式
    param:locktime Int32  时长
    return: Boolean
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    property_obj.LockCpuFreq(governor,locktime)
    time.sleep(locktime)
    return True

@checkword
def setCpuBoost(boost):
    """
    设置CPU的频率
    param:boost Boolean cpu频率
    return: Boolean
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    property_obj.SetCpuBoost(boost)
    return True


@checkword
def setCpuGovernor(governor):
    """
    设置CPU的功耗
    param:governor String cpu功耗
    return: Boolean
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    property_obj.SetCpuGovernor(governor)
    return True


@checkword
def setMode(mode):
    """
    设置电源模式
    param:mode String 电源模式
    return: Boolean
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    property_obj.SetMode(mode)
    return True


@checkword
def getBatteries():
    """
    获得所有的电池对象路径列表
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.GetBatteries()
    logging.info(result)
    if isinstance(result, dbus.Array):
        logging.info('获取所有的电池对象路径列表成功')
        return True
    else:
        logging.info('获取所有的电池对象路径列表失败')
        return False


@checkword
def refresh():
    """
    刷新电池，电源适配器（AC Adapter）的状态(充电或未充电，充满电池时间等)
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.Refresh()
    logging.info(result)
    if not result:
        logging.info('刷新电池,电源适配器状态成功')
        return True
    else:
        logging.info('刷新电池,电源适配器状态失败')
        return False


@checkword
def refreshBatteries():
    """
    刷新所有电池设备的状态
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.RefreshBatteries()
    logging.info(result)
    if not result:
        logging.info('刷新所有电池设备的状态成功')
        return True
    else:
        logging.info('刷新所有电池设备的状态失败')
        return False


@checkword
def refreshMains():
    """
    刷新电源适配器的状态
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.RefreshMains()
    logging.info(result)
    if not result:
        logging.info('刷新电源适配器的状态成功')
        return True
    else:
        logging.info('刷新电源适配器的状态失败')
        return False


@checkword
def getHasBattery():
    """
    判断是否有电池(台式机还是笔记本)
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.system.Power', 'HasBattery')
    logging.info(type(result))
    if isinstance(result, dbus.Boolean):
        logging.info('读取是否有电池值成功')
        return True
    else:
        logging.info('读取是否有电池值失败')
        return False


@checkword
def getHasLidSwitch():
    """
    判断是否能够是否有盒盖功能， 有盒盖功能为true
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.system.Power', 'HasLidSwitch')
    logging.info(result)
    if isinstance(result, dbus.Boolean):
        logging.info('读取是否有盒盖功能值成功')
        return True
    else:
        logging.info('读取是否有盒盖功能值失败')
        return False



def get_CpuBoost():
    """
    获取CPU的频率
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.system.Power', 'CpuBoost')
    logging.info(result)
    if isinstance(result, dbus.Boolean):
        logging.info('获取CPU的频率值成功')
        return result
    else:
        logging.info('获取CPU的频率值失败')
        return False

@checkword
def checkCpuBoost(boost):
    """
    检查cpu频率设置开关值
    param: boost Boolean 频率开关值
    return: Boolean
    """
    result = get_CpuBoost()
    logging.info(result)
    if result == boost :
        logging.info('设置CPU的频率值成功')
        return True
    else:
        logging.info(f'设置CPU的频率值失败，设置的值为{boost}，获取的值为{result}')
        return False


def get_CpuGovernor():
    """
    获取CPU的功耗
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.system.Power', 'CpuGovernor')
    logging.info(result)
    if isinstance(result, dbus.String):
        logging.info('获取CPU的功耗值成功')
        return result
    else:
        logging.info('获取CPU的功耗值失败')
        return False


@checkword
def checkCpuGovernor(governor):
    """
    检查cpu功耗值
    param: governor String 功耗值
    return: Boolean
    """
    result = get_CpuGovernor()
    logging.info(result)
    if result == governor :
        logging.info('设置CPU的功耗值成功')
        return True
    else:
        logging.info(f'设置CPU的功耗值失败，设置的值为{governor}，获取的值为{result}')
        return False

def get_mode():
    """
    获取电源模式
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.system.Power', 'Mode')
    logging.info(result)
    if isinstance(result, dbus.String):
        logging.info('获取电源模式成功')
        return result
    else:
        logging.info('获取电源模式值失败')
        return False

@checkword
def checkMode(mode):
    """
    检查cpu功耗值
    param: mode String 模式
    return: Boolean
    """
    result = get_mode()
    logging.info(result)
    if result == mode :
        logging.info('设置电源工作模式值成功')
        return True
    else:
        logging.info(f'设置电源工作模式值失败，设置的值为{mode}，获取的值为{result}')
        return False


@checkword
def getOnBattery():
    """
    表示是否使用电池, 使用电池时为true
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.system.Power', 'OnBattery')
    logging.info(result)
    if isinstance(result, dbus.Boolean):
        logging.info('读取是否使用电池值成功')
        return True
    else:
        logging.info('读取是否使用电池值失败')
        return False


@checkword
def getPowerSavingModeAuto():
    """
    表示使用电池时是否自动开启节能模式
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.system.Power', 'PowerSavingModeAuto')
    logging.info(result)
    if isinstance(result, dbus.Boolean):
        logging.info('读取电池是否自动开启节能模式值成功')
        return True
    else:
        logging.info('读取电池是否自动开启节能模式值失败')
        return False


@checkword
def getPowerSavingModeAutoWhenBatteryLow():
    """
    表示电池电量低时（百分比低于20%）是否自动开启节能模式
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.system.Power', 'PowerSavingModeAutoWhenBatteryLow')
    logging.info(result)
    if isinstance(result, dbus.Boolean):
        logging.info('读取电池电量低时是否自动开启节能模式值成功')
        return True
    else:
        logging.info('读取电池电量低时是否自动开启节能模式值失败')
        return False


@checkword
def getPowerSavingModeEnabled():
    """
    表示节能模式是否开启
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.system.Power', 'PowerSavingModeEnabled')
    logging.info(result)
    if isinstance(result, dbus.Boolean):
        logging.info('读取节能模式是否开启值成功')
        return True
    else:
        logging.info('读取节能模式是否开启值失败')
        return False


@checkword
def getBatteryCapacity():
    """
    表示电池充满时的电量和设计的充满时电量之比
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.system.Power', 'BatteryCapacity')
    logging.info(result)
    if isinstance(result, dbus.Double):
        logging.info('读取电量之比值成功')
        return True
    else:
        logging.info('读取电量之比值失败')
        return False


@checkword
def getBatteryPercentage():
    """
    表示电池电量百分比（笔记本）
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.system.Power', 'BatteryPercentage')
    logging.info(result)
    if isinstance(result, dbus.Double):
        logging.info('读取电池电量百分比值成功')
        return True
    else:
        logging.info('读取电池电量百分比值失败')
        return False


@checkword
def getBatteryStatus():
    """
    表示电源状态 （笔记本）
    1. "Charging"
    2. "Discharging"
    3. "Not charging"
    4. "Full"
    其他状态为Unknow,0
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.system.Power', 'BatteryStatus')
    logging.info(type(result))
    if isinstance(result, dbus.UInt32):
        logging.info('读取电源状态值成功')
        return True
    else:
        logging.info('读取电源状态值失败')
        return False


@checkword
def getPowerSavingModeBrightnessDropPercen():
    """
    表示进入节能模式后自动降低亮度百分比
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.system.Power', 'PowerSavingModeBrightnessDropPercent')
    logging.info(type(result))
    if isinstance(result, dbus.UInt32):
        logging.info('读取亮度百分比值成功')
        return True
    else:
        logging.info('读取亮度百分比值失败')
        return False


@checkword
def getBatteryTimeToEmpty():
    """
    表示电池用完的时间，单位为秒
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.system.Power', 'BatteryTimeToEmpty')
    logging.info(type(result))
    if isinstance(result, dbus.UInt64):
        logging.info('读取电池用完的时间值成功')
        return True
    else:
        logging.info('读取电池用完的时间值失败')
        return False


@checkword
def getBatteryTimeToFull():
    """
    电池充满时间，单位为秒
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.system.Power', 'BatteryTimeToFull')
    logging.info(type(result))
    if isinstance(result, dbus.UInt64):
        logging.info('读取电池充满时间值成功')
        return True
    else:
        logging.info('读取电池充满时间值失败')
        return False


if __name__ == '__main__':
    import sys

    I_g = logging.getLogger()
    I_g.setLevel(logging.DEBUG)
    s_h = logging.StreamHandler(sys.stdout)
    I_g.addHandler(s_h)
