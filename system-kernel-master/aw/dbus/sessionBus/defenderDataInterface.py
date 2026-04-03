# -*- coding: utf-8 -*-
# com.deepin.dde.controlcenter相关
import os
import time
import logging

import dbus

from aw.dbus.dbus_common import get_session_dbus_interface
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.defender.datainterface'
DBUS_PATH = '/com/deepin/defender/datainterface'
IFACE_NAME = 'com.deepin.defender.datainterface'


# ===========================
#         功能函数
# ===========================
def dbus_interface():
    return get_session_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


def get_properties_value(properties: str):
    property_obj = get_session_dbus_interface(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(IFACE_NAME, properties)
    return result


@checkword
def startApp():
    """
    defender启动服务
    :param 无
    :return:Boolearn
    """
    interface = dbus_interface()
    interface.StartApp()
    return True


@checkword
def exitApp():
    """
    defender退出服务
    :param 无
    :return:Boolearn
    """
    interface = dbus_interface()
    interface.ExitApp()
    return True


@checkword
def preInitialize():
    """
    defender 预启动
    :param 无
    :return:Boolearn
    """
    interface = dbus_interface()
    interface.preInitialize()
    return True


@checkword
def notifyAppendThreatDataByPath(sfilepath):
    """
    defender 添加流量异常数据
    :param sfilepath Srting 路径
    :return:Boolearn
    """
    interface = dbus_interface()
    result = interface.notifyAppendThreatDataByPath(sfilepath)
    if isinstance(result, dbus.Boolean):
        logging.info(result)
        return True
    else:
        logging.info(f'添加路径信息失败，返回值类型为{type(result)}')
        return False


@checkword
def notifyDeleteThreatDataByPath(sfilepath):
    """
    defender 删除流量异常数据
    :param sfilepath Srting 路径
    :return:Boolearn
    """
    interface = dbus_interface()
    result = interface.notifyDeleteThreatDataByPath(sfilepath)
    if isinstance(result, dbus.Boolean):
        logging.info(result)
        return True
    else:
        logging.info(f'删除路径信息失败，返回值类型为{type(result)}')
        return False


@checkword
def notifySelectThreatDataByPath(sfilepath):
    """
    defender 查询流量异常数据
    :param sfilepath Srting 路径
    :return:Boolearn
    """
    interface = dbus_interface()
    result = interface.notifySelectThreatDataByPath(sfilepath)
    if isinstance(result, dbus.Boolean):
        logging.info(result)
        return True
    else:
        logging.info(f'查询路径信息失败，返回值类型为{type(result)}')
        return False


@checkword
def notifySelectThreatCount():
    """
    defender 查询所有流量异常数据
    :param sfilepath Srting 路径
    :return:Boolearn
    """
    interface = dbus_interface()
    result = interface.notifySelectThreatCount()
    if isinstance(result, dbus.String):
        logging.info(result)
        return True
    else:
        logging.info(f'查询路径信息失败，返回值类型为{type(result)}')
        return False


@checkword
def getSelectThreatsCount():
    """
    defender 查询流量详情总数据量
    :param 无
    :return:Int32
    """
    interface = dbus_interface()
    result = interface.getSelectThreatsCount()
    if isinstance(result, dbus.Int32):
        logging.info(result)
        return True
    else:
        logging.info(f'获取路径信息失败，返回值类型为{type(result)}')
        return False


@checkword
def showEnginChangeNotity():
    """
    defender 发送引擎改变信号
    :param 无
    :return:Boolearn
    """
    interface = dbus_interface()
    interface.showEnginChangeNotity()
    return True


@checkword
def setFireWallSwitchStatus(status):
    """
    defender 设置防火墙总开关状态
    :param status Boolean
    :return:Boolean
    """
    interface = dbus_interface()
    interface.setFireWallSwitchStatus(status)
    return True


@checkword
def getFireWallSwitchStatus():
    """
    defender 查询流量详情总数据量
    :param 无
    :return:Int32
    """
    interface = dbus_interface()
    result = interface.getFireWallSwitchStatus()
    if isinstance(result, dbus.Boolean):
        logging.info(result)
        return True
    else:
        logging.info(f'获取防火墙开关值信息失败，返回值类型为{type(result)}')
        return False


def get_FireWallSwitchStatus():
    """
    defender 查询流量详情总数据量
    :param 无
    :return:Int32
    """
    interface = dbus_interface()
    result = interface.getFireWallSwitchStatus()
    if isinstance(result, dbus.Boolean):
        logging.info(result)
        return result
    else:
        logging.info(f'获取防火墙开关值信息失败，返回值类型为{type(result)}')
        return False

@checkword
def checkFirewallStatus(status):
    """
    检查防火墙设置的值是否生效
    param: status Boolean设置的值
    return: Boolean
    """
    result = get_FireWallSwitchStatus()
    if dbus.Boolean(result) == status:
        logging.info('检查点通过')
        return True
    else:
        logging.info(f'防火墙状态检查失败，设置的值为{status},获取到的值为{dbus.Boolean(result)}')
        return False


@checkword
def setNetControlSwitchStatus(status):
    """
    defender 设置联网管控总开关状态
    :param status Boolean
    :return:Boolean
    """
    interface = dbus_interface()
    interface.setNetControlSwitchStatus(status)
    return True


@checkword
def setRemControlSwitchStatus(status):
    """
    defender 设置远程访问总开关状态
    :param status Boolean
    :return:Boolean
    """
    interface = dbus_interface()
    interface.setRemControlSwitchStatus(status)
    return True


@checkword
def getNetAppsInfo():
    """
    defender 获得联网管控所有app数据信息
    :param: 无
    :return:Boolean
    """
    interface = dbus_interface()
    interface.getNetAppsInfo()
    return True


@checkword
def setNetControlDefaultStatus(status):
    """
    defender 设置联网管控功能所有应用初始化的默认状态
    :param status Int32
    :return:Boolean
    """
    interface = dbus_interface()
    interface.setNetControlDefaultStatus(status)
    return True


@checkword
def getNetControlDefaultStatus():
    """
    defender 得到联网管控功能所有应用初始化的默认状态
    :param 无
    :return:Int32
    """
    interface = dbus_interface()
    result = interface.getNetControlDefaultStatus()
    if isinstance(result, dbus.Int32):
        logging.info(result)
        return True
    else:
        logging.info(f'获取联网管控功能所有应用初始化的默认状态信息失败，返回值类型为{type(result)}')
        return False

def get_NetControlDefaultStatus():
    """
    defender 得到联网管控功能所有应用初始化的默认状态
    :param 无
    :return:Int32
    """
    interface = dbus_interface()
    result = interface.getNetControlDefaultStatus()
    if isinstance(result, dbus.Int32):
        logging.info(result)
        return result
    else:
        logging.info(f'获取联网管控功能所有应用初始化的默认状态信息失败，返回值类型为{type(result)}')
        return False


def checkNetCotrolDefaultStatus(status):
    """
    联网管控总开关状态检查
    param:status Boolean 开关状态
    return：Boolean

    """
    result = get_NetControlDefaultStatus()
    if result == status:
        logging.info('检查点通过')
        return True
    else:
        logging.info(f'联网管控总开关状态检查失败，设置的值为{status},获取到的值为{result}')
        return False


@checkword
def getRemAppsInfo():
    """
    defender 获得远程app数据信息
    :param: 无
    :return:Boolean
    """
    interface = dbus_interface()
    interface.getRemAppsInfo()
    return True


@checkword
def setRemControlDefaultStatus(status):
    """
    defender 设置远程访问功能所有应用初始化的默认状态
    :param status Boolean
    :return:Boolean
    """
    interface = dbus_interface()
    interface.setRemControlDefaultStatus(status)
    return True


@checkword
def getRemControlDefaultStatus():
    """
    defender 得到远程访问功能所有应用初始化的默认状态
    :param 无
    :return:Int32
    """
    interface = dbus_interface()
    result = interface.getRemControlDefaultStatus()
    if isinstance(result, dbus.Int32):
        logging.info(result)
        return True
    else:
        logging.info(f'获取远程访问功能所有应用初始化的默认状态信息失败，返回值类型为{type(result)}')

def get_RemControlDefaultStatus():
    """
    defender 得到远程访问功能所有应用初始化的默认状态
    :param 无
    :return:Int32
    """
    interface = dbus_interface()
    result = interface.getRemControlDefaultStatus()
    if isinstance(result, dbus.Int32):
        logging.info(result)
        return result
    else:
        logging.info(f'获取远程访问功能所有应用初始化的默认状态信息失败，返回值类型为{type(result)}')
        return False

@checkword
def checkRemControlDefaultStatus(status):
    """
    设置远程访问功能所有应用初始化的默认状态检查
    param:status Boolean 开关状态
    return：Boolean

    """
    result = get_RemControlDefaultStatus()
    if result == status:
        logging.info('检查点通过')
        return True
    else:
        logging.info(f'设置远程访问功能所有应用初始化的默认状态检查失败，设置的值为{status},获取到的值为{result}')
        return False

@checkword
def setRemRegisterStatus(status):
    """
    defender 设置远程访问注册状态
    :param status Boolean
    :return:Boolean
    """
    interface = dbus_interface()
    interface.setRemRegisterStatus(status)
    return True


@checkword
def getRemRegisterStatus():
    """
    defender 得到远程访问注册状态
    :param 无
    :return:Int32
    """
    interface = dbus_interface()
    result = interface.getRemRegisterStatus()
    if isinstance(result, dbus.Boolean):
        logging.info(result)
        return True
    else:
        logging.info(f'获取远程访问注册状态信息失败，返回值类型为{type(result)}')
        return False

def get_RemRegisterStatus():
    """
    defender 得到远程访问注册状态
    :param 无
    :return:Int32
    """
    interface = dbus_interface()
    result = interface.getRemRegisterStatus()
    if isinstance(result, dbus.Boolean):
        logging.info(result)
        return result
    else:
        logging.info(f'获取远程访问注册状态信息失败，返回值类型为{type(result)}')
        return False


def checkRemRegisterStatus(status):
    """
    远程注册状态检查
    param:status Boolean 开关状态
    return：Boolean

    """
    result = get_RemRegisterStatus()
    if result == status:
        logging.info('检查点通过')
        return True
    else:
        logging.info(f'远程注册检查失败，设置的值为{status},获取到的值为{result}')
        return False

@checkword
def jumpToAppStore(ntype):
    """
    defender 跳转到某个应用
    :param 无
    :return:Int32
    """
    interface = dbus_interface()
    interface.JumpToAppStore(ntype)
    return True


@checkword
def startLauncherManage():
    """
    defender 开始进行自启动管控
    :param 无
    :return:Int32
    """
    interface = dbus_interface()
    result = interface.startLauncherManage()
    if isinstance(result, dbus.Boolean):
        logging.info(result)
        return True
    else:
        logging.info(f'获取自启动管控失败，返回值类型为{type(result)}')
        return False


@checkword
def getAppsInfoEnable():
    """
    defender 获得自启动为已启动状态的所有应用
    :param 无
    :return:Int32
    """
    interface = dbus_interface()
    result = interface.getAppsInfoEnable()
    if isinstance(result, dbus.String):
        logging.info(result)
        return True
    else:
        logging.info(f'获得自启动为已启动状态的所有应用失败，返回值类型为{type(result)}')
        return False


@checkword
def getAppsInfoDisable():
    """
    defender 获得自启动为已禁止状态的所有应用
    :param 无
    :return:Int32
    """
    interface = dbus_interface()
    result = interface.getAppsInfoDisable()
    if isinstance(result, dbus.String):
        logging.info(result)
        return True
    else:
        logging.info(f'获得自启动为已禁止状态的所有应用失败，返回值类型为{type(result)}')
        return False


@checkword
def isAutostart(path):
    """
    defender 判断是否为自启动
    :param path String
    :return:Boolean
    """
    interface = dbus_interface()
    result = interface.isAutostart(path)
    if isinstance(result, dbus.Boolean):
        logging.info(result)
        return True
    else:
        logging.info(f'判断是否为自启动失败，返回值类型为{type(result)}')
        return False


@checkword
def exeAutostart(status, path):
    """
    defender 判断是否退出自启动
    :param status：Int32
    :param path：String
    :return:Boolean
    """
    interface = dbus_interface()
    result = interface.exeAutostart(status, path)
    if isinstance(result, dbus.Boolean):
        logging.info(result)
        return True
    else:
        logging.info(f'判断是否为自启动失败，返回值类型为{type(result)}')
        return False


@checkword
def notifyGetYesterdayFlowData(appname):
    """
    defender 通知去获取所有应用昨天的流量数据
    :param appname：String
    :return:Boolean
    """
    interface = dbus_interface()
    interface.notifyGetYesterdayFlowData(appname)
    return True


@checkword
def notifyGetTodayFlowData(appname):
    """
    defender 通知去获取所有应用今天的流量数据
    :param appname：String
    :return:Boolean
    """
    interface = dbus_interface()
    interface.notifyGetTodayFlowData(appname)
    return True


@checkword
def notifyGetLastMonthFlowData(appname):
    """
    defender 通知去获取所有应用上月的流量数据
    :param appname：String
    :return:Boolean
    """
    interface = dbus_interface()
    interface.notifyGetLastMonthFlowData(appname)
    return True


@checkword
def notifyGetThisMonthFlowData(appname):
    """
    defender 通知去获取所有应用这个月的流量数据
    :param appname：String
    :return:Boolean
    """
    interface = dbus_interface()
    interface.notifyGetThisMonthFlowData(appname)
    return True


@checkword
def notifyDontGetFlowData(appname):
    """
    defender 通知停止获取所有应用的流量数据
    :param appname：String
    :return:Boolean
    """
    interface = dbus_interface()
    interface.notifyDontGetFlowData(appname)
    return True


@checkword
def notifyGetAppYesterdayFlowData(appname):
    """
    defender 通知去获取某个应用昨天的流量数据
    :param appname：String
    :return:Boolean
    """
    interface = dbus_interface()
    interface.notifyGetAppYesterdayFlowData(appname)
    return True


@checkword
def notifyGetAppTodayFlowData(appname):
    """
    defender 通知去获取某个应用昨天的流量数据
    :param appname：String
    :return:Boolean
    """
    interface = dbus_interface()
    interface.notifyGetAppTodayFlowData(appname)
    return True


@checkword
def notifyGetAppLastMonthFlowData(appname):
    """
    defender 通知去获取某个应用昨天的流量数据
    :param appname：String
    :return:Boolean
    """
    interface = dbus_interface()
    interface.notifyGetAppLastMonthFlowData(appname)
    return True


@checkword
def notifyGetAppThisMonthFlowData(appname):
    """
    defender 通知去获取某个应用昨天的流量数据
    :param appname：String
    :return:Boolean
    """
    interface = dbus_interface()
    interface.notifyGetAppThisMonthFlowData(appname)
    return True


@checkword
def getAllProcInfos():
    """
    defender 获取所有进程信息列表
    :param 无
    :return:Boolean
    """
    interface = dbus_interface()
    result = interface.GetAllProcInfos()
    if isinstance(result, dbus.Array):
        logging.info(result)
        return True
    else:
        logging.info(f'获取所有进程信息列表失败，返回值类型为{type(result)}')
        return False


@checkword
def getCurrentEngine():
    """
    defender 得到当前正在使用的病毒引擎类型
    :param 无
    :return:Boolean
    """
    interface = dbus_interface()
    result = interface.GetCurrentEngine()
    if isinstance(result, dbus.Int32):
        logging.info(result)
        return True
    else:
        logging.info(f'得到当前正在使用的病毒引擎类型失败，返回值类型为{type(result)}')
        return False


@checkword
def getTrashInfoList():
    """
    defender 得到需要清理的回收站的垃圾文件列表
    :param 无
    :return:Boolean
    """
    interface = dbus_interface()
    result = interface.GetTrashInfoList()
    if isinstance(result, dbus.Array):
        logging.info(result)
        return True
    else:
        logging.info(f'得到需要清理的回收站的垃圾文件列表失败，返回值类型为{type(result)}')
        return False


@checkword
def getHistoryInfoList():
    """
    defender 得到需要清理的系统痕迹文件列表
    :param 无
    :return:Boolean
    """
    interface = dbus_interface()
    result = interface.GetHistoryInfoList()
    if isinstance(result, dbus.Array):
        logging.info(result)
        return True
    else:
        logging.info(f'得到需要清理的系统痕迹文件列表失败，返回值类型为{type(result)}')
        return False


@checkword
def getCacheInfoList():
    """
    defender 得到需要清理的系统缓存文件列表
    :param 无
    :return:Boolean
    """
    interface = dbus_interface()
    result = interface.GetCacheInfoList()
    if isinstance(result, dbus.Array):
        logging.info(result)
        return True
    else:
        logging.info(f'得到需要清理的系统缓存文件列表失败，返回值类型为{type(result)}')
        return False


@checkword
def getLogInfoList():
    """
    defender 得到需要清理的日志文件列表
    :param 无
    :return:Boolean
    """
    interface = dbus_interface()
    result = interface.GetLogInfoList()
    if isinstance(result, dbus.Array):
        logging.info(result)
        return True
    else:
        logging.info(f'得到需要清理的日志文件列表失败，返回值类型为{type(result)}')
        return False


@checkword
def getAppTrashInfoList():
    """
    defender 得到需要清理的应用程序缓存文件列表
    :param 无
    :return:Boolean
    """
    interface = dbus_interface()
    result = interface.GetAppTrashInfoList()
    if isinstance(result, dbus.String):
        logging.info(result)
        return True
    else:
        logging.info(f'得到需要清理的应用程序缓存文件列表失败，返回值类型为{type(result)}')
        return False


@checkword
def getBrowserCookiesInfoList():
    """
    defender 得到需要清理的cookies文件列表
    :param 无
    :return:Boolean
    """
    interface = dbus_interface()
    result = interface.GetBrowserCookiesInfoList()
    if isinstance(result, dbus.String):
        logging.info(result)
        return True
    else:
        logging.info(f'得到需要清理的cookies文件列表失败，返回值类型为{type(result)}')
        return False


@checkword
def requestStartTrashScan():
    """
    defender 请求开始扫描垃圾文件
    :param 无
    :return:Boolean
    """
    interface = dbus_interface()
    interface.RequestStartTrashScan()
    return True


@checkword
def deleteSpecifiedFiles(path):
    """
    defender 清理指定的用户文件
    :param path Array of String
    :return:Boolean
    """
    interface = dbus_interface()
    interface.DeleteSpecifiedFiles(path)
    return True


@checkword
def requestCleanSelectTrash():
    """
    defender 请求清理选择的垃圾文件
    :param 无
    :return:Boolean
    """
    interface = dbus_interface()
    interface.RequestCleanSelectTrash()
    return True


@checkword
def getPwdLimitPolicyEnable():
    """
    defender 获取密码限制策略开启/关闭 状态
    :param 无
    :return:Boolean
    """
    interface = dbus_interface()
    result = interface.GetPwdLimitPolicyEnable()
    if isinstance(result, dbus.Boolean):
        logging.info(result)
        return True
    else:
        logging.info(f'获取密码限制策略开启/关闭 状态失败，返回值类型为{type(result)}')
        return False

def get_PwdLimitPolicyEnable():
    """
    defender 获取密码限制策略开启/关闭 状态
    :param 无
    :return:Boolean
    """
    interface = dbus_interface()
    result = interface.GetPwdLimitPolicyEnable()
    if isinstance(result, dbus.Boolean):
        logging.info(result)
        return result
    else:
        logging.info(f'获取密码限制策略开启/关闭 状态失败，返回值类型为{type(result)}')
        return False




@checkword
def setPwdLimitPolicyEnable(enable):
    """
    defender 开启/关闭密码限制策略
    :param 无
    :return:Boolean
    """
    interface = dbus_interface()
    interface.SetPwdLimitPolicyEnable(enable)
    return True

@checkword
def checkPwdLimitPolicyEnable(enable):
    """
    密码限制策略开启/关闭 状态检查
    param:status Boolean 开关状态
    return：Boolean

    """
    result = get_PwdLimitPolicyEnable()
    if enable == True:
        if result == 1:
            logging.info('检查点通过')
            return True
        else:
            logging.info(f'设置密码限制策略开启/关闭 状态检查失败，设置的值为{enable},获取到的值为{result},类型为{type(result)}')
            return False
    if enable == False:
        if result == 0:
            logging.info('检查点通过')
            return True
        else:
            logging.info(f'设置密码限制策略开启/关闭 状态检查失败，设置的值为{enable},获取到的值为{result},类型为{type(result)}')
            return False


@checkword
def getPwdChangeError():
    """
    defender 设置密码限制等级完成信号
    :param 无
    :return:Boolean
    """
    interface = dbus_interface()
    result = interface.GetPwdChangeError()
    if isinstance(result, dbus.String):
        logging.info(result)
        return True
    else:
        logging.info(f'设置密码限制等级完成信号失败，返回值类型为{type(result)}')
        return False


#====================================属性方法===========================================

@checkword
def getScanningUsbPaths():
    """
    获取usb路径信息
    """
    result = get_properties_value(dbus.String('ScanningUsbPaths'))
    logging.info(result)
    if isinstance(result, dbus.Array):
        return True
    else:
        logging.info(f'返回类型错误，返回数据类型为{type(result)}')
        return False


@checkword
def getAllProcPidList():
    """
    获取所有Proc的Pid信息
    """
    result = get_properties_value(dbus.String('allProcPidList'))
    logging.info(result)
    if isinstance(result, dbus.Array):
        return True
    else:
        logging.info(f'返回类型错误，返回数据类型为{type(result)}')
        return False

@checkword
def getProcessInfo():
    """
    获取所有进程信息
    """
    result = get_properties_value(dbus.String('processInfo'))
    logging.info(result)
    if isinstance(result, dbus.String):
        return True
    else:
        logging.info(f'返回类型错误，返回数据类型为{type(result)}')
        return False