# -*- coding: utf-8 -*-
import dbus
import logging

from aw.dbus.sessionBus import sessionCommon
from frame.decorator import checkword

dbus_name = 'com.deepin.daemon.Audio'
dbus_path = None
iface_name = 'com.deepin.daemon.Audio.Sink'


def getDefaultSinkPath():
    """
    获取默认sink路径
    :return:sink路径
    """
    property_obj = sessionCommon.session_bus(dbus_name='com.deepin.daemon.Audio', dbus_path='/com/deepin/daemon/Audio',
                                             iface_name='org.freedesktop.DBus.Properties')
    sink_path = property_obj.Get('com.deepin.daemon.Audio', 'DefaultSink')
    logging.info(f'获取到的默认路径为:{sink_path}')
    return sink_path


@checkword
def sinkGetMeter():
    """
    返回 Meter 对象的 path,目前该方法具体逻辑未实现
    :return:True or False
    """
    dbus_path = getDefaultSinkPath()
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.GetMeter()
    logging.info(result)
    if isinstance(result, dbus.ObjectPath):
        logging.info("返回Meter对象的path成功")
        return True
    else:
        logging.info("读取Meter对象的path失败")
        return False


def sinkSetFade(value):
    """
    设置前后声道平衡值
    :return:None
    """
    dbus_path = getDefaultSinkPath()
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    property_obj.SetFade(dbus.Double(value))


def getFade():
    """
    前后声道平衡值
    :return:dbus.Double
    """
    dbus_path = getDefaultSinkPath()
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path=dbus_path,
                                             iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Audio.Sink', 'Fade')
    return result


@checkword
def checkSetFade(value):
    """
    检查设置前后声道平衡值成功
    :param value:
    :return:True or False
    """
    result = getFade()
    logging.info(result)
    if value == result:
        logging.info("检查设置前后声道平衡值成功")
        return True
    else:
        logging.info("检查设置前后声道平衡值失败")
        return False


@checkword
def getSinkFade():
    """
    读取前后声道平衡值
    :return:True or False
    """
    result = getFade()
    logging.info(type(result))
    if isinstance(result, dbus.Double):
        logging.info(f"读取Fade属性值{result}成功")
        return True
    else:
        logging.info("读取Fade属性值失败")
        return False


def sinkSetMute(value):
    """
    设置是否静音
    :return:None
    """
    dbus_path = getDefaultSinkPath()
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    property_obj.SetMute(dbus.Boolean(value))


def getMute():
    """
    获取是否静音值
    :return:dbus.Boolean
    """
    dbus_path = getDefaultSinkPath()
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path=dbus_path,
                                             iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Audio.Sink', 'Mute')
    return result


@checkword
def checkSetMute(value):
    """
    检查设置静音是否成功
    :param value:true or false
    :return:True or False
    """
    result = getMute()
    logging.info(f'获取到的设置值为{result}')
    if dbus.Boolean(value) == dbus.Boolean(result):
        logging.info("检查设置成功")
        return True
    else:
        logging.info("检查设置失败")
        return False


@checkword
def getSinkMute():
    """
    读取静音属性值
    :return:True or False
    """
    result = getMute()
    logging.info(type(result))
    if isinstance(result, dbus.Boolean):
        logging.info(f"读取Mute属性值{result}成功")
        return True
    else:
        logging.info("读取Mute属性值失败")
        return False


@checkword
def getSinkPorts():
    """
    读取支持的输出端口
    :return:True or False
    """
    dbus_path = getDefaultSinkPath()
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path=dbus_path,
                                             iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Audio.Sink', 'Ports')
    logging.info(result)
    if isinstance(result, dbus.Array):
        logging.info("读取支持的输出端口成功")
        return True
    else:
        logging.info("读取Ports属性值失败")
        return False


@checkword
def getSinkSupportBalance():
    """
    是否支持左右声道调整
    :return:True or False
    """
    dbus_path = getDefaultSinkPath()
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path=dbus_path,
                                             iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Audio.Sink', 'SupportBalance')
    logging.info(type(result))
    if isinstance(result, dbus.Boolean):
        logging.info(f"读取SupportBalance属性值{result}成功")
        return True
    else:
        logging.info("读取SupportBalance属性值失败")
        return False


@checkword
def getSinkSupportFade():
    """
    是否支持前后声道调整
    :return:True or False
    """
    dbus_path = getDefaultSinkPath()
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path=dbus_path,
                                             iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Audio.Sink', 'SupportFade')
    logging.info(type(result))
    if isinstance(result, dbus.Boolean):
        logging.info(f"获取SupportFade属性值{result}成功")
        return True
    else:
        logging.info("获取SupportFade属性值失败")
        return False


def sinkSetBalance(value, isPlay):
    """
    设置左右声道平衡
    :param value:声道平衡值
    :param isPlay:是否播放声音反馈
    :return:None
    """
    dbus_path = getDefaultSinkPath()
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    logging.info(f'设置的值为{dbus.Double(value)},{isPlay}')
    property_obj.SetBalance(dbus.Double(value), dbus.Boolean(isPlay))


def getBalance():
    """
    获取左右声道平衡值
    :return:dbus.Double
    """
    dbus_path = getDefaultSinkPath()
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path=dbus_path,
                                             iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Audio.Sink', 'Balance')
    return result


@checkword
def checkSetBalance(value):
    """
    检查设置左右声道平衡值是否成功
    :param value:声道平衡值
    :return:True or False
    """
    result = getBalance()
    ret = round(result, 2)
    logging.info(f'获取的值为{ret}')
    logging.info(f'设置的值为{value}')
    if value == ret:
        logging.info("检查设置成功")
        return True
    else:
        logging.info("检查设置失败")
        return False


@checkword
def getSinkBalance():
    """
    左右声道平衡值
    :return:True or False
    """
    result = getBalance()
    logging.info(type(result))
    if isinstance(result, dbus.Double):
        logging.info(f"读取Balance属性值{result}成功")
        return True
    else:
        logging.info("读取Balance属性值失败")
        return False


@checkword
def getSinkBaseVolume():
    """
    默认音量值
    :return:True or False
    """
    dbus_path = getDefaultSinkPath()
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path=dbus_path,
                                             iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Audio.Sink', 'BaseVolume')
    logging.info(type(result))
    if isinstance(result, dbus.Double):
        logging.info(f"读取BaseVolume属性值{result}成功")
        return True
    else:
        logging.info("读取BaseVolume属性值失败")
        return False


def sinkSetVolume(value, isPlay):
    """
    设置音量大小
    :param value:音量大小
    :param isPlay:是否播放声音反馈
    :return:None
    """
    dbus_path = getDefaultSinkPath()
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    property_obj.SetVolume(dbus.Double(value), dbus.Boolean(isPlay))


@checkword
def sinkSetPort(name):
    """
    设置此设备的当前使用端口
    :param name:此设备的当前使用端口
    :return:True or False
    """
    dbus_path = getDefaultSinkPath()
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    property_obj.SetPort(name)
    logging.info("设置此设备的当前使用端口")
    return True


def getVolume():
    """
    获取音量大小
    :return:dbus.Double
    """
    dbus_path = getDefaultSinkPath()
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path=dbus_path,
                                             iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Audio.Sink', 'Volume')
    return result


@checkword
def checkSetVolume(value):
    """
    检查设置音量大小
    :param value:音量大小
    :return:True or False
    """
    result = getVolume()
    logging.info(result)
    logging.info(value)
    if value == result:
        logging.info("检查设置成功")
        return True
    else:
        logging.info("检查设置失败")
        return False


@checkword
def getSinkVolume():
    """
    当前音量
    :return:True or False
    """
    dbus_path = getDefaultSinkPath()
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path=dbus_path,
                                             iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Audio.Sink', 'Volume')
    logging.info(type(result))
    if isinstance(result, dbus.Double):
        logging.info(f"读取Volume属性值{result}成功")
        return True
    else:
        logging.info("读取Volume属性值失败")
        return False


@checkword
def getSinkDescription():
    """
    设备描述
    :return:True or False
    """
    dbus_path = getDefaultSinkPath()
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path=dbus_path,
                                             iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Audio.Sink', 'Description')
    logging.info(type(result))
    if isinstance(result, dbus.String):
        logging.info(f"读取Description属性值{result}成功")
        return True
    else:
        logging.info("读取Description属性值失败")
        return False


@checkword
def getSinkName():
    """
    设备名
    :return:True or False
    """
    dbus_path = getDefaultSinkPath()
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path=dbus_path,
                                             iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Audio.Sink', 'Name')
    logging.info(type(result))
    if isinstance(result, dbus.String):
        logging.info(f"读取Name属性值{result}成功")
        return True
    else:
        logging.info("读取Name属性值失败")
        return False


@checkword
def getSinkActivePort():
    """
    当前使用的输出端口
    :return:True or False
    """
    dbus_path = getDefaultSinkPath()
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path=dbus_path,
                                             iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Audio.Sink', 'ActivePort')
    logging.info(type(result))
    if isinstance(result, dbus.Struct):
        logging.info(f"读取ActivePort属性值{result}成功")
        return True
    else:
        logging.info("读取ActivePort属性值失败")
        return False


@checkword
def getSinkCard():
    """
    声卡的索引
    :return:True or False
    """
    dbus_path = getDefaultSinkPath()
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path=dbus_path,
                                             iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Audio.Sink', 'Card')
    logging.info(type(result))
    if isinstance(result, dbus.UInt32):
        logging.info(f"读取Card属性值{result}成功")
        return True
    else:
        logging.info("读取Card属性值失败")
        return False
