# -*- coding: utf-8 -*-
import logging
import dbus

from aw.dbus.dbus_common import get_session_dbus_interface
from aw.dbus.sessionBus import sessionCommon
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.SessionManager'
DBUS_PATH = '/com/deepin/SessionManager'
IFACE_NAME = 'com.deepin.SessionManager'


def dbus_interface():
    return get_session_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


@checkword
def allowSessionDaemonRun():
    """
    相当于SessionManger的allowSessionDaemonRun字段的Get方法, 获得allowSessionDaemonRun的值
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.AllowSessionDaemonRun()
    if isinstance(result, dbus.Boolean):
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据不是Boolean:{type(result)}')
        return False


@checkword
def canHibernate():
    """
    对Login1.Manager.CanHibernate进行封装, 测试系统是否支持休眠。
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.CanHibernate()
    if isinstance(result, dbus.Boolean):
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据不是Boolean:{type(result)}')
        return False


@checkword
def canLogout():
    """
    返回是否能注销，目前恒为true
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.CanLogout()
    if isinstance(result, dbus.Boolean):
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据不是Boolean:{type(result)}')
        return False


@checkword
def canReboot():
    """
    通过调用Login1.Manager.CanReboot(0)测试是否能重启
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.CanReboot()
    if isinstance(result, dbus.Boolean):
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据不是Boolean:{type(result)}')
        return False


@checkword
def canShutdown():
    """
    通过调用Login1.Manager.CanPoweroff(0) 测试是否能关机
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.CanShutdown()
    if isinstance(result, dbus.Boolean):
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据不是Boolean:{type(result)}')
        return False


@checkword
def canSuspend():
    """
    根据是否有文件/sys/power/mem_sleep 判断是否能待机，如有 根据Login1.Manager.CanSuspend 测试是否能待机
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.CanSuspend()
    if isinstance(result, dbus.Boolean):
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据不是Boolean:{type(result)}')
        return False


@checkword
def getInhibitors():
    """
    遍历得到 Inhibitor 的路径列表，Inhibitor 是操作拦截器的意思，可以阻止一些由 flags 指定的操作
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.GetInhibitors()
    if isinstance(result, dbus.Array):
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据不是Array:{type(result)}')
        return False


@checkword
def isInhibited(hibit_id):
    """
    获取此 flag 代表的操作是否被拦截了,value: flag 与Inhibitor中的交集存在true则返回，否则为false
    :param:hibit_id int
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.IsInhibited(hibit_id)
    if isinstance(result, dbus.Boolean):
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据不是Boolean:{type(result)}')
        return False


@checkword
def register(str_id):
    """
    startdde 启动进程时，给进程设置 DDE_SESSION_PROCESS_COOKIE_ID 环境变量，进程（比如 kwin，dde-dock等）启动到就绪后，调用此方法以告知 startdde 进程已启动就绪
    :param:str_id: cookie id， 可从 DDE_SESSION_PROCESS_COOKIE_ID 环境变量获取
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.Register(dbus.String(str_id))
    if isinstance(result, dbus.Boolean):
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据不是Boolean:{type(result)}')
        return False


# @checkword
# def setLocked(bool_str):
#     """
#     value: true 则Lock 登陆会话，否则Unlock
#     :return:
#     """
#     interface = dbus_interface()
#     interface.SetLocked(bool_str)
#     logging.info("检查接口执行成功")
#     return True



@checkword
def toggleDebug():
    """
    根据log.LevelInfo设置Debug 模式
    :return: 无
    """
    interface = dbus_interface()
    interface.ToggleDebug()
    logging.info("检查接口执行成功")
    return True


#======================================属性================

@checkword
def getLocked():
    """
    用于判定是否Lock login会话的值
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.SessionManager', 'Locked')
    logging.info(result)
    if isinstance(result, dbus.Boolean):
        logging.info("获取Lock login会话的值成功")
        return True
    else:
        logging.info("获取Lock login会话的值失败")
        return False



@checkword
def getStage():
    """
    SessionManager 设置属性状态的值
    :return:Int32
    """
    property_obj = sessionCommon.session_bus(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.SessionManager', 'Stage')
    logging.info(result)
    if isinstance(result, dbus.Int32):
        logging.info("获取SessionManager属性状态的值成功")
        return True
    else:
        logging.info("获取SessionManager属性状态的值失败")
        return False

@checkword
def getCurrentSessionPath():
    """
    获取当前SessionManager目录
    :return:Objec Path
    """
    property_obj = sessionCommon.session_bus(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.SessionManager', 'CurrentSessionPath')
    logging.info(result)
    if isinstance(result, dbus.ObjectPath):
        logging.info("获取SessionManager目录成功")
        return True
    else:
        logging.info("取SessionManager目录失败")
        return False

@checkword
def getCurrentUid():
    """
    获取当前用户UID
    :return:String
    """
    property_obj = sessionCommon.session_bus(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    reslut = property_obj.Get('com.deepin.SessionManager', 'CurrentUid')
    logging.info(reslut)
    if isinstance(reslut, dbus.String):
        logging.info("获取用户UID成功")
        return True
    else:
        logging.info("获取用户UID成功")
        return False

