# -*- coding: utf-8 -*-
import logging

import dbus

from aw.dbus.dbus_common import get_session_dbus_interface
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.daemon.Power'
DBUS_PATH = '/com/deepin/daemon/Power'
IFACE_NAME = 'com.deepin.daemon.Power'


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
def reset():
    """
    重置所有相关设置
    :return:True or False
    """
    interface = dbus_interface()
    result = interface.Reset()
    logging.info(result)
    if not result:
        logging.info("函数执行成功")
        return True
    else:
        logging.info("函数执行异常")
        return False


@checkword
def getLinePowerScreenBlackDelay():
    """
    Int32 read/write 接通电源时，不做任何操作，到关闭屏幕需要的时间
    :return:True or False
    """
    result = get_properties_value('LinePowerScreenBlackDelay')
    if isinstance(result, dbus.Int32):
        logging.info(f"读取LinePowerScreenBlackDelay属性值为{result}s成功")
        return True
    else:
        logging.info("读取LinePowerScreenBlackDelay属性值失败")
        return False


@checkword
def getLinePowerSleepDelay():
    """
    Int32 read/write 接通电源时，不做任何操作，从黑屏到睡眠的时间 单位：秒 值为 0 时表示从不
    :return:True or False
    """
    result = get_properties_value('LinePowerSleepDelay')
    logging.info(type(result))
    if isinstance(result, dbus.Int32):
        logging.info(f"读取LinePowerSleepDelay属性值{result}s成功")
        return True
    else:
        logging.info("读取LinePowerSleepDelay属性值失败")
        return False


@checkword
def getBatteryScreenBlackDelay():
    """
    Int32 read/write 使用电池时，不做任何操作，到关闭屏幕需要的时间 单位：秒 值为 0 时表示从不
    :return:True or False
    """
    result = get_properties_value('BatteryScreenBlackDelay')
    logging.info(type(result))
    if isinstance(result, dbus.Int32):
        logging.info(f"读取BatteryScreenBlackDelay属性值{result}s成功")
        return True
    else:
        logging.info("读取BatteryScreenBlackDelay属性值失败")
        return False


@checkword
def getBatterySleepDelay():
    """
    Int32 read/write 使用电池时，不做任何操作，从黑屏到睡眠的时间 单位：秒 值为 0 时表示从不
    :return:True or False
    """
    result = get_properties_value('BatterySleepDelay')
    logging.info(type(result))
    if isinstance(result, dbus.Int32):
        logging.info(f"读取BatterySleepDelay属性值{result}s成功")
        return True
    else:
        logging.info("读取BatterySleepDelay属性值失败")
        return False


@checkword
def getScreenBlackLock():
    """
    Boolean read/write 关闭显示器前是否锁定
    :return:True or False
    """
    result = get_properties_value('ScreenBlackLock')
    logging.info(type(result))
    if isinstance(result, dbus.Boolean):
        logging.info(f"读取ScreenBlackLock属性值{result}成功")
        return True
    else:
        logging.info("读取ScreenBlackLock属性值失败")
        return False


@checkword
def getSleepLock():
    """
    Boolean read/write 睡眠前是否锁定
    :return:True or False
    """
    result = get_properties_value('SleepLock')
    logging.info(type(result))
    if isinstance(result, dbus.Boolean):
        logging.info(f"读取SleepLock属性值{result}成功")
        return True
    else:
        logging.info("读取SleepLock属性值失败")
        return False


@checkword
def getLidIsPresent():
    """
    Int32 read 是否有盖子，一般笔记本电脑才有
    :return:True or False
    """
    result = get_properties_value('LidIsPresent')
    logging.info(type(result))
    if isinstance(result, dbus.Boolean):
        logging.info(f"读取LidIsPresent属性值{result}成功")
        return True
    else:
        logging.info("读取LidIsPresent属性值失败")
        return False


@checkword
def getOnBattery():
    """
    Boolean read 是否使用电池 接通电源时为 false 使用电池时为 true
    :return:True or False
    """
    result = get_properties_value('OnBattery')
    logging.info(type(result))
    if isinstance(result, dbus.Boolean):
        logging.info(f"读取OnBattery属性值{result}成功")
        return True
    else:
        logging.info("读取OnBattery属性值失败")
        return False


@checkword
def getBatteryIsPresent():
    """
    电池是否可用
    Dict of {String,Boolean}
    read
    例如：{'BAT0':True} 表示 BAT0 可用
    :return:True or False
    """
    result = get_properties_value('BatteryIsPresent')
    logging.info(type(result))
    if isinstance(result, dbus.Dictionary):
        logging.info(f"读取BatteryIsPresent属性值{result}成功")
        return True
    else:
        logging.info("读取BatteryIsPresent属性值失败")
        return False


@checkword
def getBatteryPercentage():
    """
    Dict of {String,Double} 电池电量百分比 例如： {'BAT0': 50} 表示 电池 BAT0 的电量百分比是 50%
    :return:True or False
    """
    result = get_properties_value('BatteryPercentage')
    logging.info(type(result))
    if isinstance(result, dbus.Dictionary):
        logging.info(f"读取BatteryPercentage属性值{result}成功")
        return True
    else:
        logging.info("读取BatteryPercentage属性值失败")
        return False


@checkword
def getBatteryState():
    """
    Dict of {String,UInt32}
    电池状态
    例如：
    {'BAT0': 1L}
    表示 电池 BAT0 的状态为 1
    状态数字代表的意义：
    0 Unknown 未知
    1 Charging 充电中
    2 Discharging 不充电
    3 Empty 空
    4 FullyCharged 充满
    5 PendingCharge
    6 PendingDischarge
    :return:True or False
    """
    result = get_properties_value('BatteryState')
    logging.info(type(result))
    if isinstance(result, dbus.Dictionary):
        logging.info(f"读取BatteryState属性值{result}成功")
        return True
    else:
        logging.info("读取BatteryState属性值失败")
        return False


@checkword
def getLowPowerNotifyEnable():
    """
    低电量通知的开关，默认：关
    :return:True or False
    """
    result = get_properties_value('LowPowerNotifyEnable')
    logging.info(type(result))
    if isinstance(result, dbus.Boolean):
        logging.info(f"读取LowPowerNotifyEnable属性值{result}成功")
        return True
    else:
        logging.info("读取LowPowerNotifyEnable属性值失败")
        return False


@checkword
def getBatteryLidClosedAction():
    """
    使用电池合上盖子的操作：0:关机、1:待机（默认）、2:休眠、3:关屏、4:无操作
    :return:True or False
    """
    result = get_properties_value('BatteryLidClosedAction')
    logging.info(type(result))
    if isinstance(result, dbus.Int32):
        logging.info(f"读取BatteryLidClosedAction属性值{result}成功")
        return True
    else:
        logging.info("读取BatteryLidClosedAction属性值失败")
        return False


@checkword
def getBatteryPressPowerBtnAction():
    """
    使用电池按下电源键的操作：0:关机（默认）、1:待机、2:休眠、3:关屏、4:显示sessionUI
    :return:True or False
    """
    result = get_properties_value('BatteryPressPowerBtnAction')
    logging.info(type(result))
    if isinstance(result, dbus.Int32):
        logging.info(f"读取BatteryPressPowerBtnAction属性值{result}成功")
        return True
    else:
        logging.info("读取BatteryPressPowerBtnAction属性值失败")
        return False


@checkword
def getLinePowerLidClosedAction():
    """
    使用电池按下电源键的操作：0:关机（默认）、1:待机、2:休眠、3:关屏、4:显示sessionUI
    :return:True or False
    """
    result = get_properties_value('LinePowerLidClosedAction')
    logging.info(type(result))
    if isinstance(result, dbus.Int32):
        logging.info(f"读取LinePowerLidClosedAction属性值{result}成功")
        return True
    else:
        logging.info("读取LinePowerLidClosedAction属性值失败")
        return False


@checkword
def getLinePowerPressPowerBtnAction():
    """
    使用电源按下电源键的操作：0:关机（默认）、1:待机、2:休眠、3:关屏、4:显示sessionUI
    :return:True or False
    """
    result = get_properties_value('LinePowerPressPowerBtnAction')
    logging.info(type(result))
    if isinstance(result, dbus.Int32):
        logging.info(f"读取LinePowerPressPowerBtnAction属性值{result}成功")
        return True
    else:
        logging.info("读取LinePowerPressPowerBtnAction属性值失败")
        return False


@checkword
def getLowPowerAutoSleepThreshold():
    """
    触发自动开始睡眠的电池电量，默认值为5
    :return:True or False
    """
    result = get_properties_value('LowPowerAutoSleepThreshold')
    logging.info(type(result))
    if isinstance(result, dbus.Int32):
        logging.info(f"读取LowPowerAutoSleepThreshold属性值{result}成功")
        return True
    else:
        logging.info("读取LowPowerAutoSleepThreshold属性值失败")
        return False


@checkword
def getLowPowerAutoSleepThreshold():
    """
    触发自动开始睡眠的电池电量，默认值为5
    :return:True or False
    """
    result = get_properties_value('LowPowerAutoSleepThreshold')
    logging.info(type(result))
    if isinstance(result, dbus.Int32):
        logging.info(f"读取LowPowerAutoSleepThreshold属性值{result}成功")
        return True
    else:
        logging.info("读取LowPowerAutoSleepThreshold属性值失败")
        return False


@checkword
def getLowPowerNotifyThreshold():
    """
    触发低电量通知的电池电量，默认值为20
    :return:True or False
    """
    result = get_properties_value('LowPowerNotifyThreshold')
    logging.info(type(result))
    if isinstance(result, dbus.Int32):
        logging.info(f"读取LowPowerNotifyThreshold属性值{result}成功")
        return True
    else:
        logging.info("读取LowPowerNotifyThreshold属性值失败")
        return False


@checkword
def getAmbientLightAdjustBrightness():
    """
    是否根据环境光强度自动调整亮度
    :return:True or False
    """
    result = get_properties_value('AmbientLightAdjustBrightness')
    logging.info(type(result))
    if isinstance(result, dbus.Boolean):
        logging.info(f"读取AmbientLightAdjustBrightness属性值{result}成功")
        return True
    else:
        logging.info("读取AmbientLightAdjustBrightness属性值失败")
        return False


@checkword
def getHasAmbientLightSensor():
    """
    是否有环境光传感器
    :return:True or False
    """
    result = get_properties_value('HasAmbientLightSensor')
    logging.info(type(result))
    if isinstance(result, dbus.Boolean):
        logging.info(f"读取HasAmbientLightSensor属性值{result}成功")
        return True
    else:
        logging.info("读取HasAmbientLightSensor属性值失败")
        return False


@checkword
def getBatteryLockDelay():
    """
    使用电池时，不做任何操作，到自动锁屏的时间,单位秒。
    :return:True or False
    """
    result = get_properties_value('BatteryLockDelay')
    logging.info(type(result))
    if isinstance(result, dbus.Int32):
        logging.info(f"读取BatteryLockDelay属性值{result}成功")
        return True
    else:
        logging.info("读取BatteryLockDelay属性值失败")
        return False


@checkword
def getLinePowerLockDelay():
    """
    接通电源时，不做任何操作，到自动锁屏的时间,单位秒。
    :return:True or False
    """
    result = get_properties_value('LinePowerLockDelay')
    logging.info(type(result))
    if isinstance(result, dbus.Int32):
        logging.info(f"读取LinePowerLockDelay属性值{result}成功")
        return True
    else:
        logging.info("读取LinePowerLockDelay属性值失败")
        return False


@checkword
def getLinePowerScreensaverDelay():
    """
    接通电源时，不做任何操作，到显示屏保的时间,单位秒。
    :return:True or False
    """
    result = get_properties_value('LinePowerScreensaverDelay')
    logging.info(type(result))
    if isinstance(result, dbus.Int32):
        logging.info(f"读取LinePowerScreensaverDelay属性值{result}成功")
        return True
    else:
        logging.info("读取LinePowerScreensaverDelay属性值失败")
        return False


@checkword
def getWarnLevel():
    """
    低电量警告级别。
    0: None 无
    1: Low 低
    2: Danger 危险
    3: Critical 严重
    4: Action 行动
    :return:True or False
    """
    result = get_properties_value('WarnLevel')
    logging.info(type(result))
    if isinstance(result, dbus.UInt32):
        logging.info(f"读取WarnLevel属性值{result}成功")
        return True
    else:
        logging.info("读取WarnLevel属性值失败")
        return False


@checkword
def getBatteryScreensaverDelay():
    """
    使用电池时，不做任何操作，到显示屏保的时间，单位秒。
    :return:True or False
    """
    result = get_properties_value('BatteryScreensaverDelay')
    logging.info(type(result))
    if isinstance(result, dbus.Int32):
        logging.info(f"读取BatteryScreensaverDelay属性值{result}成功")
        return True
    else:
        logging.info("读取BatteryScreensaverDelay属性值失败")
        return False


@checkword
def getBatteryHibernateDelay():
    """
    使用电池时,不做任何操作到休眠的时间。
    :return:True or False
    """
    result = get_properties_value('BatteryHibernateDelay')
    logging.info(type(result))
    if isinstance(result, dbus.Int32):
        logging.info(f"读取BatteryHibernateDelay属性值{result}成功")
        return True
    else:
        logging.info("读取BatteryHibernateDelay属性值失败")
        return False

@checkword
def getLinePowerHibernateDelay():
    """
    使用电池时,不做任何操作到休眠的时间。
    :return:True or False
    """
    result = get_properties_value('LinePowerHibernateDelay')
    logging.info(type(result))
    if isinstance(result, dbus.Int32):
        logging.info(f"读取LinePowerHibernateDelay属性值{result}成功")
        return True
    else:
        logging.info("读取LinePowerHibernateDelay属性值失败")
        return False
'''=================设置方法========================================='''


def set_default(prop, value):
    '''
    设置接口的属性值
    :param:接口名称
    :value:指定值
    :return:无
    '''
    set_properties_value(prop, value)
    logging.info(f"将接口{prop}的值设置为{value}")
    return True
