# -*- coding: utf-8 -*-
import logging
import dbus
import time

from frame.decorator import checkword
from aw.dbus.systemBus import systemCommon
from aw.dbus.dbus_common import get_system_dbus_interface

DBUS_NAME = 'com.deepin.defender.MonitorNetFlow'
DBUS_PATH = '/com/deepin/defender/MonitorNetFlow'
IFACE_NAME = 'com.deepin.defender.MonitorNetFlow'


def dbus_interface():
    return get_system_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


def get_properties_value(properties: str):
    property_obj = get_system_dbus_interface(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(IFACE_NAME, properties)
    return result


@checkword
def Monitotr_Start():
    """
    开启服务
    :param noe:None
    :return:Boolean
    """
    interface = dbus_interface()
    interface.StartApp()
    time.sleep(2)
    return True


@checkword
def Monitotr_ExitApp():
    """
    退出服务
    :param noe:None
    :return:Boolean
    """
    interface = dbus_interface()
    interface.ExitApp()
    return True




@checkword
def getProExePath(id):
    """
    获取进程的id执行路径信息
    :param id:String 进程号
    :return Boolean
    """
    interface = dbus_interface()
    result = interface.getProExePath(id)
    logging.info(f'加密数据为:{result}')
    if isinstance(result, dbus.String):
        return True
    else:
        logging.info(f'进程执行路劲返回值类型错误，类型为:{type(result)}')
        return False


def enableNetFlowMonitor(enable):
    """
    开启/关闭进程流量监控功能
    :param enable:Boolean
    :return Boolean
    """
    interface = dbus_interface()
    interface.EnableNetFlowMonitor(enable)
    return True


@checkword
def getPocNetFlowInfos():
    """
    获取流量监控信息
    :param:None
    :return:Boolean
    """
    interface = dbus_interface()
    result = interface.GetPocNetFlowInfos()
    logging.info(f'流量信息为:{result}')
    if isinstance(result, dbus.Array):
        return True
    else:
        logging.info(f'获取流量监控信息返回值类型错误，类型为:{type(result)}')
        return False


@checkword
def setRightScanVisable(flag):
    """
    设置右键扫描的可见
    :param flag:boolean
    :return:Boolean
    """
    interface = dbus_interface()
    interface.SetRightScanVisable(flag)
    logging.info(f'设置邮件扫描是否可见')
    return True


@checkword
def setRemRegisterStatus(status):
    """
    设置ssh远程登陆端口状态
    :param status:boolean
    :return:Boolean
    """
    interface = dbus_interface()
    interface.setRemRegisterStatus(status)
    logging.info(f'设置ssh远程登陆端口状态')
    return True


@checkword
def getRemRegisterStatus():
    """
    获取ssh远程登陆端口状态
    :param :none
    :return:Boolean
    """
    interface = dbus_interface()
    result = interface.getRemRegisterStatus()
    logging.info(f'获取ssh远程登陆端口状态')
    if isinstance(result, dbus.Boolean):
        return True
    else:
        logging.info(f'获取ssh远程登陆端口状态返回值类型错误，类型为:{type(result)}')
        return False

def get_RemRegisterStatus():
    """
    获取ssh远程登陆端口状态
    :param :none
    :return:Boolean
    """
    interface = dbus_interface()
    result = interface.getRemRegisterStatus()
    logging.info(f'获取ssh远程登陆端口状态')
    if isinstance(result, dbus.Boolean):
        return result
    else:
        logging.info(f'获取ssh远程登陆端口状态返回值类型错误，类型为:{type(result)}')
        return False


def checkRemRegisterStatus(status):
    """
    检查设置状态值是否设置成功
    param: status Boolean
    return：Boolean
    """
    result = get_RemRegisterStatus()
    if result == status:
        logging.info(f'状态值检查失败，设置的值为{result}')
        return True
    else:
        logging.info(f'状态值检查失败，设置的值为{status},获取到的值为{result}')
        return False


@checkword
def clearUsbConnectionLog():
    """
    清空usb连接日志
    :param 无:boolean
    :return:Boolean
    """
    interface = dbus_interface()
    interface.ClearUsbConnectionLog()
    logging.info(f'清空usb连接日志')
    return True


@checkword
def changeIsbSaveRecord(change):
    """
    改变usb连接日志开关状态
    :param change:boolean
    :return:Boolean
    """
    interface = dbus_interface()
    interface.ChangeIsbSaveRecord(change)
    logging.info(f'改变usb连接日志开关状态')
    return True


@checkword
def selectLimitationModel(model):
    """
    选择usb限制模式
    :param model:String
    :return:Boolean
    """
    interface = dbus_interface()
    interface.SelectLimitationModel(model)
    logging.info(f'选择usb限制模式')
    return True


@checkword
def getRecordSaveSwitch():
    """
    获得usb连接日志开关状态
    :param :none
    :return:Boolean
    """
    interface = dbus_interface()
    result = interface.GetRecordSaveSwitch()
    logging.info(f'获得usb连接日志开关状态')
    if isinstance(result, dbus.Boolean):
        return True
    else:
        logging.info(f'获获得usb连接日志开关状态返回值类型错误，类型为:{type(result)}')
        return False

def get_RecordSaveSwitch():
    """
    获得usb连接日志开关状态
    :param :none
    :return:Boolean
    """
    interface = dbus_interface()
    result = interface.GetRecordSaveSwitch()
    logging.info(f'获得usb连接日志开关状态')
    if isinstance(result, dbus.Boolean):
        return result
    else:
        logging.info(f'获获得usb连接日志开关状态返回值类型错误，类型为:{type(result)}')
        return False

def checkRecordSaveSwitch(status):
    """
    检查设置状态值是否设置成功
    param: status Boolean
    return：Boolean
    """
    result = get_RecordSaveSwitch()
    if result == status:
        logging.info(f'状态值检查失败，设置的值为{result}')
        return True
    else:
        logging.info(f'状态值检查失败，设置的值为{status},获取到的值为{result}')
        return False

@checkword
def getLimitModel():
    """
    获得usb限制模式
    :param :none
    :return:Boolean
    """
    interface = dbus_interface()
    result = interface.GetLimitModel()
    logging.info(f'获得usb限制模式')
    if isinstance(result, dbus.String):
        return True
    else:
        logging.info(f'获得usb限制模式状态返回值类型错误，类型为:{type(result)}')
        return False


def get_LimitModel():
    """
    获得usb限制模式
    :param :none
    :return:Boolean
    """
    interface = dbus_interface()
    result = interface.GetLimitModel()
    logging.info(f'获得usb限制模式')
    if isinstance(result, dbus.String):
        return result
    else:
        logging.info(f'获得usb限制模式状态返回值类型错误，类型为:{type(result)}')
        return False

def checkLimitModel(model):
    """
    检查设置状态值是否设置成功
    param: model String
    return：Boolean
    """
    result = get_LimitModel()
    if result == model:
        logging.info(f'状态值检查失败，设置的值为{result}')
        return True
    else:
        logging.info(f'状态值检查失败，设置的值为{model},获取到的值为{result}')
        return False

@checkword
def getUsbConnectionRecords():
    """
    获得usb设备连接日志
    :param :none
    :return:Boolean
    """
    interface = dbus_interface()
    result = interface.GetUsbConnectionRecords()
    logging.info(f'获得usb设备连接日志')
    if isinstance(result, dbus.String):
        return True
    else:
        logging.info(f'获得usb设备连接日志返回值类型错误，类型为:{type(result)}')
        return False


@checkword
def getWhiteList():
    """
    获得usb连接白名单
    :param :none
    :return:Boolean
    """
    interface = dbus_interface()
    result = interface.GetWhiteList()
    logging.info(f'获得usb连接白名单')
    if isinstance(result, dbus.String):
        return True
    else:
        logging.info(f'获得usb连接白名单返回值类型错误，类型为:{type(result)}')
        return False


@checkword
def getDiskDevicePathList():
    """
    获取系统中储存设备/dev下路径列表
    :param :none
    :return:Boolean
    """
    interface = dbus_interface()
    result = interface.GetDiskDevicePathList()
    logging.info(f'获取系统中储存设备/dev下路径列表')
    if isinstance(result, dbus.Array):
        return True
    else:
        logging.info(f'获取系统中储存设备/dev下路径列表返回值类型错误，类型为:{type(result)}')
        return False


@checkword
def cleanSelectFile(pathlist):
    """
    清理选中的垃圾文件
    :param :none
    :return:Boolean
    """
    interface = dbus_interface()
    interface.CleanSelectFile(pathlist)
    logging.info(f'清理选中的垃圾文件')
    return True


@checkword
def cleanJournal():
    """
    清理journal文件
    :param :none
    :return:Boolean
    """
    interface = dbus_interface()
    interface.CleanJournal()
    logging.info(f'清理journal文件')
    return True


@checkword
def addSecurityLog(type,info):
    """
    添加安全日志
    :param type:Int32
    :param info:String
    :return:Boolean
    """
    interface = dbus_interface()
    interface.AddSecurityLog(type,info)
    logging.info(f'添加安全日志')
    return True


@checkword
def deleteSecurityLog(lastdate,type):
    """
    获取系统中储存设备/dev下路径列表
    :param lastdate:Int32
    :param type:Int32
    :return:Boolean
    """
    interface = dbus_interface()
    result = interface.DeleteSecurityLog(lastdate,type)
    logging.info(f'删除过滤条件下的安全日志')
    if isinstance(result, dbus.Boolean):
        return True
    else:
        logging.info(f'删除过滤条件下的安全日志返回值类型错误，类型为:{type(result)}')
        return False
