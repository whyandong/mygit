# -*- coding:utf-8 -*-
import time
import logging
import json
import dbus
import re
from aw.dbus.dbus_common import get_session_dbus_interface
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.dde.daemon.Dock'
DBUS_PATH = '/com/deepin/dde/daemon/Dock'
IFACE_NAME = 'com.deepin.dde.daemon.Dock'


# ===========================
#         功能函数
# ===========================
def dbus_interface():
    return get_session_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


def get_properties_value(properties: str):
    property_obj = get_session_dbus_interface(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(IFACE_NAME, properties)
    return result


def get_entries_path_list():
    """
    get entries path list
    :return: entries path list
    """
    result = get_properties_value('Entries')
    dbus_path_list = [str(path) for path in result]
    return dbus_path_list


def get_entry_path_by_name(entry_name="文件管理器"):
    """
    根据entry的属性值Name,获取对应的dbus path
    :param entry_name: 名称
    :return: dbus path or raise error
    """
    dbus_path_list = get_entries_path_list()
    for item in dbus_path_list:
        interface = get_session_dbus_interface(DBUS_NAME, item, iface_name='org.freedesktop.DBus.Properties')
        if entry_name == str(interface.Get('com.deepin.dde.daemon.Dock.Entry', 'Name')):
            return item
    else:
        raise ValueError(f'未找到属性Name为{entry_name}的Entry对象')


def get_window_ids_by_name(entry_name="文件管理器"):
    """
    获取entry所有窗口的id
    :param entry_name: 名称
    :return: id list
    """
    id_list = []
    dbus_path = get_entry_path_by_name(entry_name)
    interface = get_session_dbus_interface(DBUS_NAME, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = interface.Get('com.deepin.dde.daemon.Dock.Entry', 'WindowInfos')
    if isinstance(result, dbus.Dictionary) and result:
        for key in result:
            id_list.append(int(key))

    return id_list


def get_window_id_by_name(entry_name="文件管理器", index=0):
    """
    获取window的id
    :param entry_name:名称
    :param index:在列表中的index
    :return:id or raise error
    """
    id_list = get_window_ids_by_name(entry_name)
    if id_list:
        return id_list[index]
    else:
        raise ValueError('未获取到window id')


def is_docked(desktop_file='/usr/share/applications/dde-file-manager.desktop'):
    """
    是否驻留
    :param desktop_file: desktop file
    :return: True or False
    """
    result = dbus_interface().IsDocked(dbus.String(desktop_file))
    if isinstance(result, dbus.Boolean):
        logging.info(bool(result))
        return bool(result)
    else:
        logging.info(f'返回数据不是{dbus.Boolean}:{type(result)}')
        return False


def set_app_docked(desktop_file='/usr/share/applications/dde-file-manager.desktop', target=True):
    """
    设置app固定或不固定在dock状态栏
    :param desktop_file: DesktopFile文件路径字符串数组
    :param target: True: 固定,False: 不固定
    :return: True or raise error
    """
    if is_docked(desktop_file) == target:
        return True

    if target:
        dbus_interface().RequestDock(dbus.String(desktop_file), dbus.Int32(2))
    else:
        dbus_interface().RequestUndock(dbus.String(desktop_file))

    time.sleep(3)
    result = dbus_interface().IsDocked(dbus.String(desktop_file))
    if isinstance(result, dbus.Boolean) and bool(result) == target:
        return True
    else:
        logging.info(f'result_type:{type(result)},result:{target}')
        raise RuntimeError(f'设置{desktop_file}未成功,target={target}')


# ===========================
#         服务方法
# ===========================

@checkword
def cancelPreviewWindow():
    """
    取消窗口预览
    :param 无
    :return:True
    """
    interface = dbus_interface()
    interface.CancelPreviewWindow()
    return True


@checkword
def getDockedAppsDesktopFiles() -> bool:
    """
    GetDockedAppsDesktopFiles() -> ([]string desktopFiles),获取当前所有固定在dock状态栏的引用的desktopFile路径数组
    desktopFiles: DesktopFile文件路径字符串数组
    :return:True or False
    """
    result = dbus_interface().GetDockedAppsDesktopFiles()
    if isinstance(result, dbus.Array):
        for item in result:
            if isinstance(item, dbus.String):
                logging.info(str(item))
            else:
                logging.info(f'返回数据不是{dbus.Array}:{type(item)}')
                return False
        else:
            return True
    else:
        logging.info(f'返回数据不是{dbus.Array}:{type(result)}')
        return False


@checkword
def isDocked(desktop_file='/usr/share/applications/dde-file-manager.desktop'):
    """
    IsDocked(string desktopFile) -> (bool value),判断指定的应用是否固定在dock状态栏
    desktopFile: 应用的DesktopFile文件路径字符串
    value: true表示指定的应用固定在dock状态栏，false表示没有固定
    :param desktop_file: 应用的DesktopFile文件路径字符串,默认使用文件管理器
    :return:True or False
    """
    result = dbus_interface().IsDocked(dbus.String(desktop_file))
    if isinstance(result, dbus.Boolean):
        logging.info(bool(result))
        return True
    else:
        logging.info(f'返回数据不是{dbus.Boolean}:{type(result)}')
        return False


@checkword
def isOnDock(desktop_file='/usr/share/applications/dde-file-manager.desktop'):
    """
    IsOnDock(string desktopFile) -> (bool value),判断指定的应用是否固定在dock状态栏，或者是否正在运行并且在dock栏存在关联icon参数
    desktopFile: 应用的DesktopFile文件路径字符串
    value: true表示固定在dock状态栏，或者运行并在dock栏存在关联icon
    :param desktop_file: 应用的DesktopFile文件路径字符串,默认使用文件管理器
    :return:True or False
    """
    result = dbus_interface().IsOnDock(dbus.String(desktop_file))
    if isinstance(result, dbus.Boolean):
        logging.info(bool(result))
        return True
    else:
        logging.info(f'返回数据不是{dbus.Boolean}:{type(result)}')
        return False


@checkword
def getEntryIDs():
    """
    GetEntryIDs() -> (string[] list),获取当前停靠在dock栏上的所有的引用id列表
    list: 应用的id字符串数组，id如deepin-music, google-chrome等等
    :return:True or False
    """
    result = dbus_interface().GetEntryIDs()
    if isinstance(result, dbus.Array):
        for item in result:
            if isinstance(item, dbus.String):
                logging.info(str(item))
            else:
                logging.info(f'返回数据不是{dbus.Array}:{type(item)}')
                return False
        else:
            return True
    else:
        logging.info(f'返回数据不是{dbus.Array}:{type(result)}')
        return False


@checkword
def getPluginSettings():
    """
    获取插件配置
    :param 无
    :return:String
    """
    result = dbus_interface().GetPluginSettings()
    if isinstance(result, dbus.String):
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据不是{dbus.String}:{type(result)}')
        return False


def get_getPluginSettings():
    """
    获取插件配置
    :param 无
    :return:String
    """
    result = dbus_interface().GetPluginSettings()
    if isinstance(result, dbus.String):
        logging.info(result)
        return result
    else:
        logging.info(f'返回数据不是{dbus.String}:{type(result)}')
        return False


@checkword
def activateWindow(win_id):
    """
    ActivateWindow(uint32 win),激活给定窗口id的已经打开的窗口，通常会使该窗口成为焦点窗口
    win: 窗口id，如何获取请查看Entry对象的WindowInfos属性
    :param win_id: 窗口id
    :return:True
    """
    dbus_interface().ActivateWindow(dbus.UInt32(win_id))
    return True


@checkword
def closeWindow(win_id):
    """
    CloseWindow(win uint32),关闭给定id的窗口实例
    win: 请参考ActivateWindow函数的win参数
    :param win_id: 窗口id
    :return:True
    """
    dbus_interface().CloseWindow(dbus.UInt32(win_id))
    return True


@checkword
def maximizeWindow(win_id):
    """
    MaximizeWindow(win uint32),最大化给定id的窗口实例，首先会调用ActivateWindow激活窗口再使之最大化
    win: 请参考ActivateWindow函数的win参数
    :param win_id: 窗口id
    :return:True
    """
    dbus_interface().MaximizeWindow(dbus.UInt32(win_id))
    return True


@checkword
def minimizeWindow(win_id):
    """
    MinimizeWindow(win uint32),最小化给定id的窗口实例
    win: 请参考ActivateWindow函数的win参数
    :param win_id: 窗口id
    :return:True
    """
    dbus_interface().MinimizeWindow(dbus.UInt32(win_id))
    return True


@checkword
def moveEntry(index, newindex):
    """
    移动应用位置
    :param index int32起始位置
    :param newindex 新位置
    :return:True
    """
    interface = dbus_interface()
    interface.MoveEntry()
    return True


@checkword
def moveWindow(win):
    """
    移动窗口位置
    :param win 新位置
    :return:True
    """
    interface = dbus_interface()
    interface.MoveWindow(win)
    return True


@checkword
def previewWindow(win):
    """
    预览窗口
    :param win 新位置
    :return:True
    """
    interface = dbus_interface()
    interface.PreviewWindow(win)
    return True


@checkword
def queryWindowIdentifyMethod(wid):
    """
    查询窗口鉴别方式
    :param : wid：窗口id
    :return:String
    """
    result = dbus_interface().QueryWindowIdentifyMethod(wid)
    logging.info(result)
    if isinstance(result, dbus.String):
        logging.info(f'返回数据类型正常{dbus.String}:{type(result)}')
        return True
    else:
        logging.info(f'返回数据不是{dbus.String}:{type(result)}')
        return False


@checkword
def makeWindowAbove(win_id):
    """
    MakeWindowAbove(win uint32),使给定id的窗口处于桌面最上层位置，首先会调用ActivateWindow激活窗口再设置处于桌面最上层显示参数
    win: 请参考ActivateWindow函数的win参数
    :param win_id: 窗口id
    :return:True
    """
    dbus_interface().MakeWindowAbove(dbus.UInt32(win_id))
    return True


def requestDock(desktop_file='/usr/share/applications/dde-file-manager.desktop', index=2):
    """
    RequestDock(string desktopFile, int32 index) -> (bool ok),请求应用的desktop文件路径驻留在dock上
    desktopFile: 应用的desktop文件路径
    index: 驻留在dock上的应用位置索引，从左往右从0开始
    ok: 发送成功为true，否则失败
    :param desktop_file: 应用的DesktopFile文件路径字符串,默认使用文件管理器
    :param index: 驻留在dock上的应用位置索引，从左往右从0开始,默认为2
    :return: 返回的数据,执行状态码  0为返回数据正确，1为返回数据正确
    """
    result = dbus_interface().RequestDock(dbus.String(desktop_file), dbus.Int32(index))
    if isinstance(result, dbus.Boolean):
        logging.info(bool(result))
        return bool(result), 0
    else:
        logging.info(f'返回数据不是{dbus.Boolean}:{type(result)}')
        return result, 1


def requestUndock(desktop_file='/usr/share/applications/dde-file-manager.desktop'):
    """
    RequestUndock(string desktopFile) -> (bool ok),取消驻留在dock上的应用的desktop文件路径参数
    desktopFile: 应用的desktop文件路径
    ok: 取消成功为true，否则失败
    :param desktop_file: 应用的DesktopFile文件路径字符串,默认使用文件管理器
    :return:返回的数据,执行状态码  0为返回数据正确，1为返回数据正确
    """
    result = dbus_interface().RequestUndock(dbus.String(desktop_file))
    if isinstance(result, dbus.Boolean):
        logging.info(bool(result))
        return bool(result), 0
    else:
        logging.info(f'返回数据不是{dbus.Boolean}:{type(result)}')
        return result, 1


@checkword
def setFrontendWindowRect(x, y, width, height):
    """
    设置窗口设置窗口Rect
    :param x int32
    :param y int32
    :param width Uint32
    :param height Uint32
    :return:True
    """
    interface = dbus_interface()
    interface.SetFrontendWindowRect(x, y, width, height)
    return True


@checkword
def setPluginSettings(jsonStr):
    """
    设置窗口设置窗口Rect
    :param jsonStr String
    :return:True
    """
    interface = dbus_interface()
    interface.SetPluginSettings(jsonStr)
    return True


@checkword
def mergePluginSettings(jsonStr):
    """
    合并窗口插件Rect
    :param jsonStr String
    :return:True
    """
    interface = dbus_interface()
    result = interface.MergePluginSettings(jsonStr)
    logging.info(result)
    return True


@checkword
def checkPluginSettings(jsonStr):
    """
    检验合并窗口插件后，插件配置数据是否生效;部分机型的插件参数个数不一致，需要校验{XXX}中设置参数是以子串存在
    :param jsonStr String：自定义插件数据匹配时，需要去掉首尾字符
    :return:True
    """
    result = get_getPluginSettings()
    logging.info(result)
    json1 = re.split(r'[{}]', jsonStr)
    result1 = re.split(r'[{}]', result)
    if isinstance(result, dbus.String):
        for i in range(1,len(json1)-2):
            if json1[i] in result1[i]:
                pass
            else:
                logging.info(f"返回数据未生效,子串值{json1[i]}不存在于{result1[i]}")
                return False
        logging.info(f"返回数据类型正常{dbus.String}，且合并插件生效{jsonStr}")
        return True
    else:
        logging.info(f"返回数据不是{dbus.String}:{type(result)}")
        return False


@checkword
def removePluginSettings(keylist):
    """
    移除子插件设置;
    :param key1:单个子插件配置；keylist：插件列表配置
    :return: 无
    """
    keylist_ = keylist.split(',')
    print(keylist_)
    for key in keylist_:
        logging.info(key)
        result = dbus_interface().RemovePluginSettings(key, keylist)
        logging.info(result)
    return True

# ===========================
#         服务属性
# ===========================
@checkword
def entries():
    """
    []objectPath Entries (read)
    在com.deepin.dde.daemon.Dock服务下，针对每个打开的应用并且在dock上有相应icon显示，dock模块会生成一个
    entires并关联一个接口/com/deepin/dde/daemon/Dock/entries/xx，Entries存储的就是所有的关联接口列表
    :return:True or False
    """
    result = get_properties_value('Entries')
    if isinstance(result, dbus.Array):
        for item in result:
            if isinstance(item, dbus.ObjectPath):
                logging.info(str(item))
            else:
                logging.info(f'返回数据不是{dbus.ObjectPath}:{type(item)}')
                return False
        else:
            return True
    else:
        logging.info(f'返回数据不是{dbus.Array}:{type(result)}')
        return False


@checkword
def hideMode():
    """
    int32 HideMode (read/write)
    隐藏模式，对应dock的三个状态值，0表示dock一直显示，1表示dock一直隐藏，3表示智能隐藏
    该属性由dde-dock前端程序通过dbus属性设置
    :return:True or False
    """
    result_list = [0, 1, 3]
    result = get_properties_value('HideMode')
    if isinstance(result, dbus.Int32):
        if int(result) in result_list:
            logging.info(int(result))
            return True
        else:
            logging.info(f'返回的结果不是{result_list}中的任何一种,请检查接口是否有变动')
            return False
    else:
        logging.info(f'返回数据不是{dbus.Int32}:{type(result)}')
        return False


@checkword
def hideState():
    """
    int32 HideState (read)
    当前dock隐藏状态，0表示未知状态，1表示dock显示，2表示dock隐藏
    前端dde-dock监听该属性改变事件，根据监听到的值控制dock显示或者隐藏
    :return:True or False
    """
    result_list = [0, 1, 2]
    result = get_properties_value('HideState')
    if isinstance(result, dbus.Int32):
        if int(result) in result_list:
            logging.info(int(result))
            return True
        else:
            logging.info(f'返回的结果不是{result_list}中的任何一种,请检查接口是否有变动')
            return False
    else:
        logging.info(f'返回数据不是{dbus.Int32}:{type(result)}')
        return False


@checkword
def dockedApps(app_id='/S@deepin-app-store'):
    """
    []string DockedApps:当前dock栏驻留的应用包名称列表
    :param app_id: 检查app是否docked,默认检查雷鸟邮件
    :return:True or False
    """
    result = get_properties_value(dbus.String('DockedApps'))
    if isinstance(result, dbus.Array):
        if result:
            for item in result:
                if isinstance(item, dbus.String):
                    logging.info(item)
                    if app_id == str(item):
                        return True
                else:
                    return False
            else:
                return True
        else:
            logging.info('检查到无任何软件驻留在dock,请确认系统默认方案')
            return False
    else:
        logging.info('返回数据类型不匹配')
        logging.info(f'返回数据类型为：{type(result)}')
        return False


@checkword
def opacity():
    """
    double Opacity:当前dock栏透明度，默认0.4
    :return:True or False
    """
    result = get_properties_value(dbus.String('Opacity'))
    if isinstance(result, dbus.Double):
        logging.info(F'当前dock栏透明度{result}')
        return True
    else:
        logging.info('返回数据类型不匹配')
        logging.info(f'返回数据类型为：{type(result)}')
        return False


@checkword
def displayMode():
    """
    int32 DisplayMode:当前dock栏显示模式，0表示时尚模式，1表示高效模式
    :return:True or False
    """
    _ = {0: "时尚模式", 1: "高效模式"}
    result = get_properties_value(dbus.String('DisplayMode'))
    if isinstance(result, dbus.Int32):
        logging.info(F'当前dock栏显示模式{result},{_[int(result)]}')
        return True
    else:
        logging.info('返回数据类型不匹配')
        logging.info(f'返回数据类型为：{type(result)}')
        return False


@checkword
def position():
    """
    int32 Position:当前屏幕dock栏所在位置，0表示屏幕上方，1表示屏幕右边，2表示屏幕下方，3表示屏幕左边
    :return:True or False
    """
    _ = {0: "屏幕上方", 1: "屏幕右边", 2: "屏幕左边"}
    result = get_properties_value(dbus.String('Position'))
    if isinstance(result, dbus.Int32):
        logging.info(F'当前屏幕dock栏所在位置{result},{_[int(result)]}')
        return True
    else:
        logging.info('返回数据类型不匹配')
        logging.info(f'返回数据类型为：{type(result)}')
        return False


@checkword
def frontendWindowRect():
    """
    Rect FrontendWindowRect:当前dock栏形状大小
    Rect 的定义:
            {
                X, Y          int32
                Width, Height uint32
            }
    字段含义:
            X, Y: 矩形X、Y坐标点
            Width, Height：矩形宽、高值
    :return:True or False
    """
    _ = (dbus.Int32, dbus.Int32, dbus.UInt32, dbus.UInt32)
    result = get_properties_value(dbus.String('FrontendWindowRect'))
    if isinstance(result, dbus.Struct):
        new_tuple = zip(result, _)
        for item in new_tuple:
            if isinstance(item[0], item[1]):
                logging.info(item[0])
            else:
                return False
        return True
    else:
        logging.info('返回数据类型不匹配')
        logging.info(f'返回数据类型为：{type(result)}')
        return False


def get_frontendWindowRect():
    """
    Rect FrontendWindowRect:当前dock栏形状大小
    Rect 的定义:
            {
                X, Y          int32
                Width, Height uint32
            }
    字段含义:
            X, Y: 矩形X、Y坐标点
            Width, Height：矩形宽、高值
    :return:True or False
    """
    _ = (dbus.Int32, dbus.Int32, dbus.UInt32, dbus.UInt32)
    result = get_properties_value(dbus.String('FrontendWindowRect'))
    if isinstance(result, dbus.Struct):
        new_tuple = zip(result, _)
        for item in new_tuple:
            if isinstance(item[0], item[1]):
                logging.info(item[0])
            else:
                return False
        logging.info(f'result:{result}')
        return result
    else:
        logging.info('返回数据类型不匹配')
        logging.info(f'返回数据类型为：{type(result)}')
        return False


@checkword
def windowSizeEfficient():
    """
    uint32 WindowSizeEfficient:高效模式下dock栏高度，调节范围40～100
    :return:True or False
    """
    result = get_properties_value(dbus.String('WindowSizeEfficient'))
    if isinstance(result, dbus.UInt32):
        logging.info(F'高效模式下dock栏高度{result}')
        return True
    else:
        logging.info('返回数据类型不匹配')
        logging.info(f'返回数据类型为：{type(result)}')
        return False


@checkword
def windowSizeFashion():
    """
    uint32 WindowSizeFashion:时尚模式下dock栏高度，调节范围40～100
    :return:True or False
    """
    result = get_properties_value(dbus.String('WindowSizeFashion'))
    if isinstance(result, dbus.UInt32):
        logging.info(F'时尚模式下dock栏高度{result}')
        return True
    else:
        logging.info('返回数据类型不匹配')
        logging.info(f'返回数据类型为：{type(result)}')
        return False
