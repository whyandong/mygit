# -*- coding: utf-8 -*-
import dbus
import logging

from aw.dbus.sessionBus import sessionCommon
from frame.decorator import checkword

dbus_name = 'com.deepin.daemon.Audio'
dbus_path = '/com/deepin/daemon/Audio'
iface_name = 'com.deepin.daemon.Audio'
iface_name2 = 'com.deepin.sync.Config'


@checkword
def getCards():
    """
    获取声卡信息
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Audio', 'Cards')
    logging.info(result)
    if isinstance(result, dbus.String):
        logging.info("获取声卡信息成功")
        return True
    else:
        logging.info("获取声卡信息失败")
        return False


@checkword
def getReduceNoise():
    """
    是否打开降噪开关，如果打开，将调用webrtc为物理设备建立虚拟通道，达到降噪效果，关闭则声音效果和原来一致
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Audio', 'ReduceNoise')
    logging.info(result)
    if isinstance(result, dbus.Boolean):
        logging.info("获取降噪开关状态成功")
        return True
    else:
        logging.info("获取降噪开关状态失败")
        return False


@checkword
def getCardsWithoutUnavailable():
    """
    获取可用的音频设备端口信息
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Audio', 'CardsWithoutUnavailable')
    logging.info(result)
    if isinstance(result, dbus.String):
        logging.info("获取可用音频设备端口信息成功")
        return True
    else:
        logging.info("获取可用音频设备端口信息失败")
        return False


def isPortEnabled(cardId, portName):
    """
    获取音频端口的启用/禁用状态
    :param cardId:声卡 id
    :param portName:端口名
    :return:result
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.IsPortEnabled(cardId, portName)
    logging.info(result)
    return result


@checkword
def checkIsPortEnabled(cardId, portName):
    """
    检查获取音频端口的启用/禁用状态是否成功
    :param cardId:声卡 id
    :param portName:端口名
    :return: True or False
    """
    ret = isPortEnabled(cardId, portName)
    if isinstance(ret, dbus.Boolean):
        logging.info('取音频端口的启用/禁用状态成功')
        return True
    else:
        logging.info('取音频端口的启用/禁用状态失败')
        return False


def setPortEnabled(cardId, portName, mode):
    """
    启用/禁用音频端口
    :param cardId:声卡 id
    :param portName:端口名
    :param mode: enable or disable
    :return:None
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    if mode == 'enable':
        logging.info("启用音频端口")
        property_obj.SetPortEnabled(cardId, portName, dbus.Boolean(True))
    elif mode == 'disable':
        logging.info("禁用音频端口")
        property_obj.SetPortEnabled(cardId, portName, dbus.Boolean(False))
    else:
        logging.info("传入参数错误，请检查！")

@checkword
def setPort(cardId, portName, direction):
    """
    设置端口
    :param cardId:声卡 id
    :param portName:端口名
    :param direction: 方向 Unint32
    :return:None
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)

    property_obj.SetPortEnabled(cardId, portName, direction)

    return True


@checkword
def checkSetPortEnabledStatus(cardId, portName, mode):
    """
    检查设置启用/禁用音频端口状态
    :param cardId:声卡 id
    :param portName:端口名
    :param mode:enable or disable
    :return:True or False
    """
    ret = isPortEnabled(cardId, portName)
    if mode == 'enable':
        if ret:
            logging.info("检查启用音频端口成功")
            return True
        else:
            logging.info('检查启用音频端口失败')
            return False
    elif mode == 'disable':
        if not ret:
            logging.info("检查禁用音频端口成功")
            return True
        else:
            logging.info("检查禁用音频端口失败")
            return False
    else:
        logging.info("传入参数错误，请检查！")
        return False


@checkword
def noRestartPulseAudio():
    """
    用于设置不自动重启 pulseaudio 服务
    :return:True
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    property_obj.NoRestartPulseAudio()
    logging.info("检查接口执行成功")
    return True


@checkword
def reset():
    """
    用于重置输入输出设备的音量以及sound-effect的开关.
    :return:True
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    property_obj.Reset()
    logging.info("检查接口执行成功")
    return True


@checkword
def getSinks():
    """
    输出设备的dbus路径的集合
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Audio', 'Sinks')
    logging.info(result)
    if isinstance(result, dbus.Array):
        logging.info("输出设备的dbus路径的集合成功")
        return True
    else:
        logging.info("输出设备的dbus路径的集合失败")
        return False


@checkword
def getSinkInputs():
    """
    指向 sink 输入内容的音频流dbus路径的集合
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Audio', 'SinkInputs')
    logging.info(result)
    if isinstance(result, dbus.Array):
        logging.info("获取指向sink输入内容的音频流dbus路径的集合成功")
        return True
    else:
        logging.info("获取指向sink输入内容的音频流dbus路径的集合失败")
        return False


@checkword
def getSources():
    """
    输入设备的dbus路径的集合
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Audio', 'Sources')
    logging.info(result)
    if isinstance(result, dbus.Array):
        logging.info("获取输入设备的dbus路径的集合成功")
        return True
    else:
        logging.info("获取输入设备的dbus路径的集合失败")
        return False


@checkword
def getIncreaseVolume():
    """
    最大音量控制开关 如果是true 最大音量为150% 如果是false 最大音量为100%
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Audio', 'IncreaseVolume')
    logging.info(type(result))
    if isinstance(result, dbus.Boolean):
        logging.info(f'读取IncreaseVolume属性值{result}成功')
        return True
    else:
        logging.info("读取IncreaseVolume属性值失败")
        return False


@checkword
def getMaxUIVolume():
    """
    最大UI音量与 IncreaseVolume 有关.IncreaseVolume如果是true,最大音量为150%,IncreaseVolume如果是false,最大音量为100%
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Audio', 'MaxUIVolume')
    logging.info(type(result))
    if isinstance(result, dbus.Double):
        logging.info(f'读取MaxUIVolume属性值{result}成功')
        return True
    else:
        logging.info("读取MaxUIVolume属性值失败")
        return False


@checkword
def getDefaultSink():
    """
    默认 Sink 对象的路径
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Audio', 'DefaultSink')
    logging.info(type(result))
    if isinstance(result, dbus.ObjectPath):
        logging.info(f'读取DefaultSink属性值{result}成功')
        return True
    else:
        logging.info("读取DefaultSink属性值失败")
        return False


@checkword
def getDefaultSource():
    """
    默认 Source 对象的路径
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Audio', 'DefaultSource')
    logging.info(type(result))
    if isinstance(result, dbus.ObjectPath):
        logging.info(f'读取DefaultSource属性值{result}成功')
        return True
    else:
        logging.info("读取DefaultSource属性值失败")
        return False

def getsyncConfig():
    """
    获取同步配置Config
    :return:Array of [Byte] data
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name=iface_name2)
    result = property_obj.Get()
    logging.info(result)
    return result

@checkword
def get_syncConfig():
    """
    获取同步配置Config，判断数据类型是否正常
    :return:Array of [Byte] data
    """
    result = getsyncConfig()
    if isinstance(result, dbus.Array) and isinstance(result[0], dbus.Byte):
        logging.info(f'获取sync配置信息类型正常')
        return True
    else:
        logging.info(f"获取sync配置信息类型异常，返回值类型为{type(result)}")
        return False

def convertByte(str):
    byte_array = []
    for i in range(len(str)):
        s = bytes(str[i], encoding='utf-8')
        byte_array.append(s)
    return byte_array

@checkword
def setsyncConfig(config):
    """
    设置同步配置Config
    :params:Array of [Byte] data
    :return:无
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name=iface_name2)
    result = property_obj.Set(dbus.Array(config))
    logging.info(result)
    return True

@checkword
def checksyncConfig(config):
    """
    获取同步配置Config，判断数据类型是否正常
    :return:Array of [Byte] data
    """
    result = getsyncConfig()
    for i in range(len(result)):
        if str(result[i]) == str(config[i]):
            pass
        else:
            logging.info(f"获取sync配置信息{str(result[i])}不一致，原设置值{str(config[i])}")
            return False
    logging.info("获取sync配置信息一致，生效正常")
    return True