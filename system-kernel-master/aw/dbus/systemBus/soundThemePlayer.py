# -*- coding: utf-8 -*-
import re
import time
import logging
import subprocess

import dbus

from frame.decorator import checkword


def excute_cmd(cmd):
    """
    执行cmd命令
    :param cmd:输入命令
    :return:string
    """
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, encoding='utf-8')

    outMsg = p.stdout.read()
    errMsg = p.stderr.read()
    if errMsg:
        return errMsg
    else:
        return outMsg


def system_bus(dbus_name='com.deepin.api.SoundThemePlayer', dbus_path='/com/deepin/api/SoundThemePlayer',
               iface_name='com.deepin.api.SoundThemePlayer'):
    system_bus = dbus.SystemBus()
    system_obj = system_bus.get_object(dbus_name, dbus_path)
    property_obj = dbus.Interface(system_obj, dbus_interface=iface_name)
    return property_obj


def enableSoundDesktopLogin(mode):
    """
    设置开机音效开关
    :param mode: enable or disable
    :return:None
    """
    time.sleep(2)
    property_obj = system_bus()
    if mode == 'enable':
        logging.info("打开开机音效")
        property_obj.EnableSoundDesktopLogin(True)
    elif mode == 'disable':
        logging.info("关闭开机音效")
        property_obj.EnableSoundDesktopLogin(False)
    else:
        logging.info("传入值无效")


@checkword
def checkSoundDesktopLoginStatus(mode):
    """
    检查音效开关状态
    :param mode:enable or disable
    :return:True or False
    """
    time.sleep(2)
    cmd = 'cat /var/lib/deepin-sound-player/config-1000.json'
    logging.info(cmd)
    out = excute_cmd(cmd)
    logging.info(out)
    res = re.findall(r'"DesktopLoginEnabled":(\S*?),', out)[0]
    logging.info(res)
    if mode == 'enable':
        if res == 'true':
            logging.info("检查打开音效成功")
            return True
        else:
            logging.info("检查打开音效失败")
            return False
    elif mode == 'disable':
        if res == 'false':
            logging.info("检查关闭音效成功")
            return True
        else:
            logging.info("检查关闭音效失败")
            return False


def play(theme, event, device):
    """
    播放指定主题、事件和设备的音效
    :param theme:默认为deepin
    :param event:音效关联的事件名称，可读取sessionbus的com.deepin.daemon.SoundEffect.GetSoundEnabledMap
    :param device:参数内容为"plughw:CARD=%s,DEV=%s"，其中%s字段替换为上述/var/lib/deepin-sound-player/config-%d.json文件里相应的值即可
    :return:None
    """
    time.sleep(2)
    property_obj = system_bus()
    dbus_out = property_obj.Play(theme, event, device)
    logging.info("返回值：{}".format(str(dbus_out)))


def playSoundDesktopLogin():
    """
    播放系统登录音效
    :return:None，可听到开机音效
    """
    time.sleep(2)
    property_obj = system_bus()
    dbus_out = property_obj.PlaySoundDesktopLogin()
    logging.info("返回值：{}".format(str(dbus_out)))


@checkword
def saveAudioState():
    """
    获取当前停靠在dock栏上的所有的引用id列表，目前仅仅是写入设置参数到配置文件，无实际功能效果
    :param activePlayback:设置设备的参数信息，格式为{"card": string类型, "device": string类型, mute:bool类型}
    card和device的值可以在终端用命令 aplay -L列表所有的音频设备信息
    :return:True or False
    """
    time.sleep(2)
    activePlayback = {"card": 'HDMI', "device": '3', "mute": dbus.Boolean(False)}
    property_obj = system_bus()
    dbus_out = property_obj.SaveAudioState(activePlayback)
    logging.info(dbus_out)
    out = excute_cmd('aplay -L|grep DEV=3')
    logging.info(out)
    if out:
        logging.info("设置参数成功")
        return True
    else:
        logging.info("设置参数失败")
        return False


def setSoundTheme(theme):
    """
    设置声音主题
    :param theme:主题名称，会把新主题名称写入/var/lib/deepin-sound-player/config-%d.json配置文件
    :return:None
    """
    time.sleep(2)
    property_obj = system_bus()
    dbus_out = property_obj.SetSoundTheme(theme)
    logging.info("返回值：{}".format(str(dbus_out)))


@checkword
def checksetSoundTheme(theme):
    """
    检查声音主题
    :return:True or False
    """
    time.sleep(2)
    cmd = 'cat /var/lib/deepin-sound-player/config-*.json'
    logging.info(cmd)
    out = excute_cmd(cmd)
    logging.info(out)
    res = re.findall(r'"Theme":"(\S*?)",', out)[0]
    logging.info(res)
    if res == theme:
        logging.info("检查设置声音主题成功")
        return True
    else:
        logging.info("检查设置声音主题失败")
        return False
