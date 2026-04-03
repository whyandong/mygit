# -*- coding: utf-8 -*-
import time
import logging

import dbus

from aw.dbus.dbus_common import get_session_dbus_interface
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.daemon.SoundEffect'
IFACE_NAME = 'com.deepin.daemon.SoundEffect'
DBUS_PATH = '/com/deepin/daemon/SoundEffect'


def dbus_interface():
    return get_session_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


def get_properties_value(properties: str):
    property_obj = get_session_dbus_interface(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(IFACE_NAME, properties)
    return result


def get_sound_enable_map():
    interface = dbus_interface()
    result = interface.GetSoundEnableMap()
    # sound_list = [str(path) for path in result]
    return result


'''======================方法封装＝＝＝＝＝＝＝＝＝＝＝＝'''


@checkword
def enableSound(name, enabled):
    """
    param:name:String:音频名称
    param:enabled:Boolean:开启或关闭
    """
    interface = dbus_interface()
    interface.EnableSound(name, enabled)
    logging.info("检查接口执行成功")
    return True


@checkword
def getSoundEnabledMap():
    """
    param:无
    return:DICT,音频名称和路径文件组成的字典
    """
    interface = dbus_interface()
    result = interface.GetSoundEnabledMap()
    if isinstance(result, dbus.Dictionary):
        logging.info(f"获取音频信息的值成功,map值为{result}")
        return True
    else:
        logging.info(f"获取音频信息的值失败,map值为{result}")
        return False
    return True

@checkword
def getSoundFile(name):
    """
    根据传入的音频名称获取对应的播放声音文件路径
    param:name:音频名称
    return:String 文件路径
    """
    interface = dbus_interface()
    result = interface.GetSoundFile(name)
    logging.info(f"获取到的声音路径名为{result}")
    if isinstance(result, dbus.String):
        logging.info(f"获取音频文件路{name}径成功")
        return True
    else:
        logging.info(f"获取音频文件路径失败")
        return False

@checkword
def getSystemSoundFile(name):
    """
        根据传入的音频名称获取对应的播放声音文件路径
        param:name:音频名称
        return:String 文件路径
    """
    interface = dbus_interface()
    result = interface.GetSystemSoundFile(name)
    logging.info(f"获取到的声音路径名为{result}")
    if isinstance(result, dbus.String):
        logging.info(f"获取音频文件路{name}径成功")
        return True
    else:
        logging.info(f"获取音频文件路径失败")
        return False

@checkword
def isSoundEnabled(name):
    """
    根据传入的音频文件名称，判断是开启或关闭状态
    param:name:String:音频名称
    return:Boolean:状态
    """
    interface = dbus_interface()
    result = interface.IsSoundEnabled(name)
    logging.info(f"获取到的声音路径名为{result}")
    if isinstance(result, dbus.Boolean):
        logging.info(f"音频{name}径成功")
        return True
    else:
        logging.info(f"获取音频文件路径失败")
        return False

@checkword
def playSound(name):
    """
    播放传入的音频名称
    param:name:String:音频名称
    return:无
    """
    interface = dbus_interface()
    interface.PlaySound(name)
    logging.info("播放成功")
    return True


@checkword
def playSystemSound(name):
    """
    播放传入的系统音频名称
    param:name:String:音频名称
    return:无
    """
    interface = dbus_interface()
    interface.PlaySystemSound(name)
    logging.info("播放成功")
    return True


'''======================属性方法====================='''


@checkword
def getEnabled():
    """
    bool Enabled (read):当前音频的开关状态
    :param :无
    :return:True or False
    """
    result = get_properties_value(dbus.String('Enabled'))
    if isinstance(result, dbus.Boolean):
        logging.info(f'当前entry关联的程序是否处于焦点激活状态:{bool(result)}')
        return True

    else:
        logging.info('返回数据类型不匹配')
        logging.info(f'返回的数据类型为{type(result)}')
        return False
