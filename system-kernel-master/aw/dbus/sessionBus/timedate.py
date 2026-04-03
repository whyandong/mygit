# -*- coding: utf-8 -*-
import time
import dbus
import logging

from aw.dbus.sessionBus import sessionCommon
from frame.decorator import checkword

dbus_name = 'com.deepin.daemon.Timedate'
dbus_path = '/com/deepin/daemon/Timedate'
iface_name = 'com.deepin.daemon.Timedate'


@checkword
def addUserTimezone(zone):
    """
    添加指定的时间区域到用户的时间区域列表中
    :param zone: 时间区域
    :return: True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.AddUserTimezone(zone)
    logging.info(result)
    if not result:
        logging.info("添加时间区域设置成功")
        return True
    else:
        logging.info("添加时间区域设置失败")
        return False


@checkword
def deleteUserTimezone(zone):
    """
    从用户的时间区域列表中删除指定的时间区域
    :param zone: 时间区域
    :return: True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.DeleteUserTimezone(zone)
    logging.info(result)
    if not result:
        logging.info("删除时间区域设置成功")
        return True
    else:
        logging.info("删除时间区域设置失败")
        return False


@checkword
def getSampleNTPServers():
    """
    获得NTPServer服务样本
    :return: True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.GetSampleNTPServers()
    logging.info(result)
    if isinstance(result, dbus.Array):
        logging.info("获得NTPServer服务样本成功")
        return True
    else:
        logging.info("获得NTPServer服务样本失败")
        return False


@checkword
def getZoneInfo(zone):
    """
    获得时间区域相关信息
    :param zone: 时间区域
    :return: True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.GetZoneInfo(zone)
    logging.info(result)
    if isinstance(result, dbus.Struct):
        logging.info("获得时间区域相关信息成功")
        return True
    else:
        logging.info("获得时间区域相关信息失败")
        return False


@checkword
def getZoneList():
    """
    获取区域时间列表
    :return: True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.GetZoneList()
    logging.info(result)
    if isinstance(result, dbus.Array):
        logging.info("获取区域时间列表成功")
        return True
    else:
        logging.info("获取区域时间列表失败")
        return False


def reset():
    """
    重置系统时间和网络时间同步
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.Reset()
    time.sleep(5)
    logging.info(result)


def setDate(year, month, day, hour, min, sec, nsec):
    """
    设置系统时间和日期
    :param year:年
    :param month:月
    :param day:日
    :param hour:时
    :param min:分
    :param sec:秒
    :param nsec:毫微秒
    :return:None
    """
    time.sleep(1)
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    property_obj.SetDate(year, month, day, hour, min, sec, nsec)
    time.sleep(2)


def getTimeInfo():
    """
    获取timedatectl命令执行的输出，得到字典
    :return:dict
    """
    out = sessionCommon.excute_cmd('timedatectl')
    logging.info(out)
    info_dict = {}
    time_list = out.strip().split('\n')
    for i in range(0, 4):
        line_list = time_list[i].strip().split(':', 1)
        info_dict[line_list[0]] = line_list[1]
    logging.info(info_dict)
    return info_dict


@checkword
def checkSetDateStatus(month, day):
    """
    检查设置日期状态
    :param month: 月
    :param day: 日
    :return: True or False
    """
    out = getTimeInfo()
    local_time = out['Local time']
    logging.info(local_time)
    if str(month) in local_time and str(day) in local_time:
        logging.info("检查设置时间成功")
        return True
    else:
        logging.info("检查设置时间失败")
        return False


def setNTP(useNTP):
    """
    设置是否使用NTP
    :param useNTP:True or False
    :return:None
    """
    time.sleep(1)
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    property_obj.SetNTP(dbus.Boolean(useNTP))
    time.sleep(6)


def ntp():
    """
    获取ntp属性值
    :return:result
    """
    time.sleep(1)
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Timedate', 'NTP')
    logging.info(result)
    return result


@checkword
def checkNTPStatus(mode):
    """
    检查NTP设置状态
    :param mode:enable or disable
    :return:True or False
    """
    ret = ntp()
    if mode == 'enable':
        if ret:
            logging.info("检查设置使用NTP成功")
            return True
        else:
            logging.info("检查设置使用NTP失败")
            return False
    elif mode == 'disable':
        if not ret:
            logging.info("设置不使用NTP成功")
            return True
        else:
            logging.info("设置不使用NTP失败")
            return False


@checkword
def getNTP():
    """
    获取ntp属性值并检查获取成功
    :return: True or False
    """
    ret = ntp()
    if ret == 0 or ret == 1:
        logging.info("获取NTP值成功")
        return True
    else:
        logging.info("获取NTP值失败")
        return False


def setLocalRTC(passwd, localRTC, fixSystem):
    """
    是否使用当地实时时间（不能用sudo执行，普通用户执行弹框，需要对UI处理，暂时不开发）
    :param localRTC:true 为设置当地实时时间, false 为使用UTC时间标准
    :param fixSystem:true or false
    :return:None
    """
    pass


@checkword
def getLocalRTC():
    """
    获取本地时间设置RTC属性值
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Timedate', 'LocalRTC')
    logging.info(result)
    if isinstance(result, dbus.Boolean):
        logging.info("获取本地时间RTC属性值成功")
        return True
    else:
        logging.info("获取本地时间RTC属性值失败")
        return False


@checkword
def setTime(usec, relative):
    """
    设置当前时间
    :param usec:自1970年1月1日零时起， 到当前时间的微秒数
    :param relative:true 表示将 usec 加到系统时间上， false 表示将 usec 设置为系统时间
    :return:True or False
    :examlpe:60000000, True or 1595505311000000, False
    """
    time.sleep(2)
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.SetTime(dbus.Int64(usec), dbus.Boolean(relative))
    logging.info(result)
    if not result:
        logging.info('设置当前时间成功')
        return True
    else:
        logging.info("设置当前时间失败")
        return False


@checkword
def getUserTimezones():
    """
    获取用户添加的时间区域列表
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Timedate', 'UserTimezones')
    logging.info(result)
    if isinstance(result, dbus.Array):
        logging.info("获取用户添加的时间区域列表成功")
        return True
    else:
        logging.info("获取用户添加的时间区域列表失败")
        return False


@checkword
def getCanNTP():
    """
    是否能使用NTP时间服务器
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Timedate', 'CanNTP')
    logging.info(result)
    if isinstance(result, dbus.Boolean):
        logging.info("获取是否能使用NTP时间服务器值成功")
        return True
    else:
        logging.info("获取是否能使用NTP时间服务器值失败")
        return False


@checkword
def getCanNTP():
    """
    是否能使用NTP时间服务器
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Timedate', 'CanNTP')
    logging.info(result)
    if isinstance(result, dbus.Boolean):
        logging.info("获取是否能使用NTP时间服务器值成功")
        return True
    else:
        logging.info("获取是否能使用NTP时间服务器值失败")
        return False


@checkword
def getUse24HourFormat():
    """
    是否使用24小时时间制
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Timedate', 'Use24HourFormat')
    logging.info(result)
    if isinstance(result, dbus.Boolean):
        logging.info("获取是否使用24小时时间制值成功")
        return True
    else:
        logging.info("获取是否使用24小时时间制值失败")
        return False


@checkword
def getDSTOffset():
    """
    夏令时偏移量
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Timedate', 'DSTOffset')
    logging.info(result)
    if isinstance(result, dbus.Int32):
        logging.info("获取夏令时偏移量值成功")
        return True
    else:
        logging.info("获取夏令时偏移量值失败")
        return False


@checkword
def getDSTOffset():
    """
    夏令时偏移量
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Timedate', 'DSTOffset')
    logging.info(result)
    if isinstance(result, dbus.Int32):
        logging.info("获取夏令时偏移量值成功")
        return True
    else:
        logging.info("获取夏令时偏移量值失败")
        return False


@checkword
def getLongDateFormat():
    """
    长日期格式
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Timedate', 'LongDateFormat')
    logging.info(result)
    if isinstance(result, dbus.Int32):
        logging.info("获取长日期格式值成功")
        return True
    else:
        logging.info("获取长日期格式值失败")
        return False


@checkword
def getLongTimeFormat():
    """
    长时间格式
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Timedate', 'LongTimeFormat')
    logging.info(result)
    if isinstance(result, dbus.Int32):
        logging.info("获取长时间格式值成功")
        return True
    else:
        logging.info("获取长时间格式值失败")
        return False


@checkword
def getShortDateFormat():
    """
    短日期格式
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Timedate', 'ShortDateFormat')
    logging.info(result)
    if isinstance(result, dbus.Int32):
        logging.info("获取短日期格式值成功")
        return True
    else:
        logging.info("获取短日期格式值失败")
        return False


@checkword
def getShortTimeFormat():
    """
    短时间格式
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Timedate', 'ShortTimeFormat')
    logging.info(result)
    if isinstance(result, dbus.Int32):
        logging.info("获取短时间格式值成功")
        return True
    else:
        logging.info("获取短时间格式值失败")
        return False


@checkword
def getWeekBegins():
    """
    星期开始时间
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Timedate', 'WeekBegins')
    logging.info(result)
    logging.info(type(result))
    if isinstance(result, dbus.Int32):
        logging.info("获取星期开始时间值成功")
        return True
    else:
        logging.info("获取星期开始时间值失败")
        return False


@checkword
def getWeekdayFormat():
    """
    星期格式
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Timedate', 'WeekdayFormat')
    logging.info(result)
    logging.info(type(result))
    if isinstance(result, dbus.Int32):
        logging.info("获取星期格式值成功")
        return True
    else:
        logging.info("获取星期格式值失败")
        return False


@checkword
def getNTPServer():
    """
    网络时间协议服务器
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Timedate', 'NTPServer')
    logging.info(result)
    if isinstance(result, dbus.String):
        logging.info("获取网络时间协议服务器值成功")
        return True
    else:
        logging.info("获取网络时间协议服务器值失败")
        return False


@checkword
def getTimezone():
    """
    网络时间协议服务器
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Timedate', 'Timezone')
    logging.info(result)
    if isinstance(result, dbus.String):
        logging.info("获取时间区域值成功")
        return True
    else:
        logging.info("获取时间区域值失败")
        return False


if __name__ == '__main__':
    import sys

    I_g = logging.getLogger()
    I_g.setLevel(logging.DEBUG)
    s_h = logging.StreamHandler(sys.stdout)
    I_g.addHandler(s_h)
