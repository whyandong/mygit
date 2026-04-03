# -*- coding: utf-8 -*-
# com.deepin.dde.daemon.Launcher相关
import os
import time
import logging

import dbus

from aw.dbus.sessionBus import sessionCommon

DBUS_NAMEN = 'com.deepin.dde.daemon.Launcher'
DBUS_PATH = '/com/deepin/dde/daemon/Launcher'
IFACE_NAME = 'com.deepin.dde.daemon.Launcher'


def start_monitor_signal(member):
    dbus_monitor = sessionCommon.DbusMonitor(DBUS_NAMEN, DBUS_PATH, member)
    dbus_monitor.start()
    return dbus_monitor


def stop_monitor_signal(dbus_monitor: sessionCommon.DbusMonitor):
    dbus_monitor.stop()


def parse_stop_monitor_signal(dbus_monitor: sessionCommon.DbusMonitor):
    return dbus_monitor.parse()


def is_in_apps(app_id: str = 'dde-file-manager'):
    property_obj = sessionCommon.session_bus(DBUS_NAMEN, DBUS_PATH, IFACE_NAME)
    all_item_info = property_obj.GetAllItemInfos()
    logging.info(f'{"=" * 20}系统和当前用户所有应用程序的信息{"=" * 20}')
    for struct in all_item_info:
        if struct[2] == dbus.String(app_id):
            logging.info(f'{app_id}在应用程序列表中')
            return True
    else:
        logging.info(f'{app_id}不在在应用程序列表中')
        return False


def getPropertiesValue(properties: str):
    property_obj = sessionCommon.session_bus(DBUS_NAMEN, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(DBUS_NAMEN, properties)
    return result


def getAllItemInfos() -> bool:
    """
    GetAllItemInfos: 获取系统和当前用户所有应用程序的信息
    方式：判读返回值类型,Array of [Struct of (String, String, String, String, Int64, Int64)]
    对应字段：
            {
            string path
            string name
            string id
            string icon
            int64 categoryId
            int64 timeInstalled
            }
    字段含义：
            path：路径
            name： 名称,用于界面展示
            id： 程序 id
            icon：图标
            categoryId： 分类 id
            timeInstalled：安装时间,是 unix 时间戳
    :return: True or False
    """
    property_obj = sessionCommon.session_bus(DBUS_NAMEN, DBUS_PATH, IFACE_NAME)
    all_item_info = property_obj.GetAllItemInfos()
    tpyes = (dbus.String, dbus.String, dbus.String, dbus.String, dbus.Int64, dbus.Int64)
    logging.info(f'{"=" * 20}系统和当前用户所有应用程序的信息{"=" * 20}')
    for struct in all_item_info:
        zipped = zip(struct, tpyes)
        for itme in zipped:
            if isinstance(itme[0], itme[1]):
                logging.info(f'{itme[1]}: {itme[0]}')
            else:
                return False
        else:
            logging.info(f'=' * 50)
    else:
        logging.info(f'{"=" * 20}系统和当前用户所有应用程序的信息{"=" * 20}')
        return True


def getAllNewInstalledApps() -> bool:
    """
    GetAllNewInstalledApps: 获取最近新安装的app列表
    方式：判读返回值类型,Array of [String]
    :return: True or False
    """
    property_obj = sessionCommon.session_bus(DBUS_NAMEN, DBUS_PATH, IFACE_NAME)
    all_new_installed_apps = property_obj.GetAllNewInstalledApps()
    logging.info(f'{"=" * 20}最近新安装的app列表{"=" * 20}')
    for itme in all_new_installed_apps:
        if isinstance(itme, dbus.String):
            logging.info(f'id: {itme}')
        else:
            return False
    else:
        logging.info(f'{"=" * 20}最近新安装的app列表{"=" * 20}')
        return True


def getDisableScaling(app_id: str = 'dde-file-manager', target: bool = False) -> bool:
    """
    GetDisableScaling (string id) -> (bool value): 获取id对应的程序是否禁用缩放,true表示禁用,false表示不禁用
    :param app_id: 对应程序的id,可以使用GetAllItemInfos接口获得,默认检查文件管理器
    :param target: 预期结果,文件管理器默认是可以缩放
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(DBUS_NAMEN, DBUS_PATH, IFACE_NAME)
    is_scaling = property_obj.GetDisableScaling(dbus.String(app_id))
    if isinstance(is_scaling, dbus.Boolean):
        if dbus.Boolean(target) == is_scaling:
            logging.info(f'is_scaling: {is_scaling}')
            return True
        else:
            logging.info(f'请检查{app_id}是否可以缩放')
            return False
    else:
        logging.info('返回的数据类型有误')
        return False


def getItemInfo(app_id: str = 'dde-file-manager') -> bool:
    """
    GetItemInfo (string id) -> (ItemInfo itemInfo):获取id对应的程序的详细信息
    各字段详细信息参见getAllItemInfos
    :param app_id:对应程序的id,可以使用GetAllItemInfos接口获得,默认检查文件管理器
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(DBUS_NAMEN, DBUS_PATH, IFACE_NAME)
    item_info = property_obj.GetItemInfo(dbus.String(app_id))
    tpyes = (dbus.String, dbus.String, dbus.String, dbus.String, dbus.Int64, dbus.Int64)
    zipped = zip(item_info, tpyes)
    logging.info(f'=' * 50)
    for itme in zipped:
        if isinstance(itme[0], itme[1]):
            logging.info(f'{itme[1]}: {itme[0]}')
        else:
            return False
    else:
        logging.info(f'=' * 50)
        return True


def getUseProxy(app_id: str = 'dde-file-manager') -> bool:
    """
    GetUseProxy (string id) -> (bool value):获取id对应的程序是否使用代理,true表示使用代理,false表示不使用
    :param app_id:应程序的id,可以使用GetAllItemInfos接口获得,默认检查文件管理器
    :return:True or False
    """
    logging.info(f'检查{app_id}是否能使用代理')
    property_obj = sessionCommon.session_bus(DBUS_NAMEN, DBUS_PATH, IFACE_NAME)
    is_use_proxy = property_obj.GetUseProxy(dbus.String(app_id))
    if isinstance(is_use_proxy, dbus.Boolean):
        logging.info(f'is_use_proxy: {is_use_proxy},结果符合预期')
        return True
    else:
        logging.info(f'返回的数据类型有误,type:{type(is_use_proxy)}')
        return False


def isItemOnDesktop(app_id: str = 'dde-file-manager', target: bool = False) -> bool:
    """
    IsItemOnDesktop (string id) -> (bool result):获取id对应的程序是否有桌面图标,true表示桌面有图标,false表示没有
    :param app_id:应程序的id,可以使用GetAllItemInfos接口获得,默认检查文件管理器
    :param target:预期结果,文件管理器默认无图标
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(DBUS_NAMEN, DBUS_PATH, IFACE_NAME)
    is_item_on_desktop = property_obj.IsItemOnDesktop(dbus.String(app_id))
    if isinstance(is_item_on_desktop, dbus.Boolean):
        if dbus.Boolean(target) == is_item_on_desktop:
            logging.info(f'is_item_on_desktop: {is_item_on_desktop}')
            return True
        else:
            logging.info(f'请检查{app_id}是否存在桌面图标')
            return False
    else:
        logging.info('返回的数据类型有误')
        return False


# def markLaunched(app_id: str = 'dde-file-manager'): #暂不开发
#     property_obj = sessionCommon.session_bus(DBUS_NAMEN, DBUS_PATH, IFACE_NAME)
#     property_obj.MarkLaunched(dbus.String(id))

def requestRemoveFromDesktop(app_id: str = 'dde-file-manager', is_exists: bool = True, ignore: bool = False):
    """
    RequestRemoveFromDesktop (string id) -> (bool ok):请求将指定id的程序桌面图标删除,执行结果,true表示成功,id没有桌面图标则报错
    :param app_id:应程序的id,可以使用GetAllItemInfos接口获得,默认检查文件管理器
    :param is_exists:桌面图标是否存在
    :param ignore:忽视错误,设置此值可作为功能函数
    :return:True or False
    """
    try:
        property_obj = sessionCommon.session_bus(DBUS_NAMEN, DBUS_PATH, IFACE_NAME)
        property_obj.RequestRemoveFromDesktop(dbus.String(app_id))
        if ignore:
            return True

        if is_exists:
            logging.info(f'{app_id}图标存在未报错,与预期相符')
            return True
        else:
            logging.info(f'{app_id}图标不存在未报错,与预期不相符')
            return False

    except dbus.exceptions.DBusException as e:
        message = e.get_dbus_message()
        home_path = os.environ['HOME']
        if f'remove {home_path}/Desktop/{app_id}.desktop: no such file or directory' != message:  # 判断报错信息
            raise e

        if ignore:
            return True

        if is_exists:
            logging.info(f'{app_id}图标存在但报错,与预期不符')
            return False  # 存在但报错,与预期不符
        else:
            logging.info(f'{app_id}图标不存在但报错,与预期相符')
            return True  # 不存在但报错,与预期相符


def requestSendToDesktop(app_id: str = 'dde-file-manager', is_exists: bool = False, is_clear: bool = True,
                         ignore: bool = False):
    """
    RequestSendToDesktop (string id) -> (bool ok):请求将指定id的程序创建桌面图标,执行结果,true表示成功,id已经有桌面图标则报错
    :param app_id:应程序的id,可以使用GetAllItemInfos接口获得,默认检查文件管理器
    :param is_exists:面图标是否存在
    :param is_clear:设置前是否进行清理
    :param ignore:忽视错误,设置此值可作为功能函数
    :return:True or False
    """
    if is_clear:
        requestRemoveFromDesktop(app_id, ignore=True)
        time.sleep(3)
        is_exists = False
    try:
        property_obj = sessionCommon.session_bus(DBUS_NAMEN, DBUS_PATH, IFACE_NAME)
        property_obj.RequestSendToDesktop(dbus.String(app_id))
        if ignore:
            return True
        if is_exists:
            logging.info(f'{app_id}图标存在未报错,与预期不相符')
            return False
        else:
            logging.info(f'创建{app_id}图标成功')
            return True

    except dbus.exceptions.DBusException as e:
        message = e.get_dbus_message()
        if 'file already exists' != message:
            raise e
        if ignore:
            return True

        if is_exists:
            logging.info(f'{app_id}图标存在但报错,与预期相符')
            return True  # 存在但报错,与预期相符
        else:
            logging.info(f'{app_id}图标不存在但报错,与预期不符')
            return False  # 不存在但报错,与预期不符


def setDisableScaling(app_id: str = 'dde-file-manager', value: bool = False) -> bool:
    """
    SetDisableScaling (string id, bool value) :设置指定id的程序是否禁用缩放
    :param app_id:应程序的id,可以使用GetAllItemInfos接口获得,默认检查文件管理器
    :param value:是否禁用缩放
    :return: True or False
    """
    property_obj = sessionCommon.session_bus(DBUS_NAMEN, DBUS_PATH, IFACE_NAME)
    property_obj.SetDisableScaling(dbus.String(app_id), dbus.Boolean(value))
    return getDisableScaling(app_id=app_id, target=value)


def setUseProxy(app_id: str = 'dde-file-manager', value: bool = False):
    """
    SetUseProxy (String id, Boolean value) ↦ ():设置指定id的程序是否使用代理
    :param app_id:应程序的id,可以使用GetAllItemInfos接口获得,默认检查文件管理器
    :param value:是否使用代理
    :return:True or False
    """
    logging.info(f'设置{app_id}是否使用代理,设置值为{value}')
    property_obj = sessionCommon.session_bus(DBUS_NAMEN, DBUS_PATH, IFACE_NAME)
    property_obj.SetUseProxy(dbus.String(app_id), dbus.Boolean(value))


def search(app_id: str = 'music'):
    """
    Search (String key) ↦ ():开始菜单中搜索应用程序
    :param app_id:被搜索的关键字,默认搜索文件管理器
    :return:True or False
    """
    logging.info(f'开始菜单中搜索应用程序{app_id}')
    property_obj = sessionCommon.session_bus(DBUS_NAMEN, DBUS_PATH, IFACE_NAME)
    property_obj.Search(dbus.String(app_id))


# def requestUninstall(app_id: str = 'youdao-dict', purge: bool = True): #发生报错
#     """
#     RequestUninstall(string id, bool purge):请求将指定id的程序卸载安装
#     id:应用程序id
#     purge:无实际意义
#     :param app_id:被卸载程序的id,默认卸载有道词典,执行前请先安装有道词典
#     :param purge:无实际意义
#     :return:
#     """
#     logging.info(f'请求将id为{app_id}的程序卸载安装')
#     property_obj = sessionCommon.session_bus(DBUS_NAMEN, DBUS_PATH, IFACE_NAME)
#     property_obj.RequestUninstall(dbus.String(app_id), dbus.Boolean(purge))


def fullscreen() -> bool:
    """
    bool Fullscreen(read/write):开始菜单是否全屏显示：true-全屏显示、false-菜单显示
    :return:True or False
    """
    logging.info(f'读取{IFACE_NAME}属性Fullscreen的值')
    result = getPropertiesValue(dbus.String('Fullscreen'))
    if isinstance(result, dbus.Boolean):
        logging.info(f'返回的数据类型为：{type(result)}')
        logging.info(f'result:{result}')
        return True
    else:
        logging.info(f'返回的数据类型与预期不符')
        logging.info(f'返回的数据类型为：{type(result)}')
        logging.info(f'result:{result}')
        return False


def displayMode() -> bool:
    """
    int32 DisplayMode(read/write),开始菜单里面图标的显示模式：0-全部显示、1-分类显示，全屏模式时生效。
    :return:True or False
    """
    logging.info(f'读取{IFACE_NAME}属性Fullscreen的值')
    result = getPropertiesValue(dbus.String('DisplayMode'))
    if isinstance(result, dbus.Int32):
        logging.info(f'返回的数据类型为：{type(result)}')
        logging.info(f'result:{result}')
        return True
    else:
        logging.info(f'返回的数据类型与预期不符')
        logging.info(f'返回的数据类型为：{type(result)}')
        logging.info(f'result:{result}')
        return False


def itemChanged(dbus_monitor: sessionCommon.DbusMonitor, *parse_flgs: str):
    """
    ItemChanged(string status,  ItemInfo itemInfo, int64 CategoryID):应用程序安装，更新，卸载时触发该消息
    :param dbus_monitor: sessionCommon.DbusMonitor类的实例,且已运行start
    :param parse_flgs: 检查用字符串,判断此字符串在不在返回的结果中
    :return:True or False
    """
    result = dbus_monitor.parse()
    logging.info(f'ItemChanged result:\n{result}')
    for parse_flg in parse_flgs:
        logging.info(f'ItemChanged parse_flg:\n{parse_flg}')
        if parse_flg in result:
            logging.info('parse_flg在result中')
        else:
            logging.info('parse_flg不在result,请检查此接口')
            return False
    else:
        return True


def searchDone(dbus_monitor: sessionCommon.DbusMonitor, parse_flg: str):
    """
    SearchDone([]string apps):Search方法执行完之后触发,apps:搜索匹配到的应用程序
    :param dbus_monitor:sessionCommon.DbusMonitor类的实例,且已运行start
    :param parse_flg:检查用字符串,判断此字符串在不在返回的结果中
    :return:True or False
    """
    result = dbus_monitor.parse()
    logging.info(f'SearchDone parse_flg:\n{parse_flg}')
    logging.info(f'SearchDone result:\n{result}')
    if parse_flg in result:
        logging.info('parse_flg在result中')
        return True
    else:
        logging.info('parse_flg不在result,请检查此接口')
        return False
