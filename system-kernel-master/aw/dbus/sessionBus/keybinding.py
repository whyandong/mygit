# -*- coding: utf-8 -*-
import logging
import dbus
import time
from aw.dbus.dbus_common import get_session_dbus_interface
from aw.dbus.sessionBus import sessionCommon
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.daemon.Keybinding'
DBUS_PATH = '/com/deepin/daemon/Keybinding'
IFACE_NAME = 'com.deepin.daemon.Keybinding'


def dbus_interface():
    return get_session_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


@checkword
def reset():
    """
    重置个性化设置为默认设置参数
    :return:True or False
    """
    interface = dbus_interface()
    interface.Reset()
    logging.info("检查接口执行成功")
    return True


@checkword
def selectKeystroke():
    """
    暂停快捷键响应进行快捷键设置
    :return:True or False
    """
    interface = dbus_interface()
    interface.SelectKeystroke()
    time.sleep(2)
    interface.SelectKeystroke()
    logging.info("检查接口执行成功")
    return True


def selectKeystroke_tear():
    """
    暂停快捷键响应进行快捷键设置
    :return:True or False
    """
    interface = dbus_interface()
    interface.SelectKeystroke()
    time.sleep(2)
    interface.SelectKeystroke()
    logging.info("检查接口执行成功")


@checkword
def getListAllShortcuts():
    """
    获取快捷键列表
    :return:True or False
    """
    interface = dbus_interface()
    result = interface.ListAllShortcuts()
    if isinstance(result, dbus.String):
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据不是String:{type(result)}')
        return False


@checkword
def getListShortcutsByType(shortcut_type):
    """
    获取指定类型的快捷键列表
    :param shortcut_type:
    :return:True or False
    """
    interface = dbus_interface()
    result = interface.ListShortcutsByType(shortcut_type)
    if isinstance(result, dbus.String):
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据不是String:{type(result)}')
        return False


@checkword
def shortcutSwitchLayout():
    """
    切换键盘布局快捷键的flag
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Keybinding', 'ShortcutSwitchLayout')
    logging.info(result)
    if isinstance(result, dbus.UInt32):
        logging.info("切换键盘布局快捷键的flag成功")
        return True
    else:
        logging.info("切换键盘布局快捷键的flag失败")
        return False


@checkword
def getNumLockState():
    """
    获取NumLock的状态，返回int32类型数据
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Keybinding', 'NumLockState')
    logging.info(result)
    if isinstance(result, dbus.Int32):
        logging.info("获取当前NumLock的状态成功")
        return True
    else:
        logging.info("获取当前NumLock的状态失败")
        return False


def getNumLockStateNumber():
    """
    获取NumLock的状态，返回状态值
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Keybinding', 'NumLockState')
    logging.info(result)
    return result


@checkword
def setNumLockState(state):
    """
    设置NumLock的状态
    :param state:状态，0关闭、1开启
    :return:True or False
    """
    interface = dbus_interface()
    interface.SetNumLockState(state)
    logging.info("检查接口执行成功")
    return True


@checkword
def checksetNumLockState(state):
    """
    检查NumLock状态是否设置成功
    :param state: 设置的状态值
    :return: True or False
    """
    ret = getNumLockStateNumber()
    logging.info(f'ret: {ret}')
    if ret == state:
        logging.info("检查NumLock状态成功")
        return True
    else:
        logging.info("检查NumLock状态失败")
        return False


@checkword
def setCapsLockState(state):
    """
    设置CapsLock的状态
    :param state:状态，0关闭、1开启
    :return:True or False
    """
    interface = dbus_interface()
    interface.SetCapsLockState(state)
    logging.info("检查接口执行成功")
    return True


@checkword
def searchShortcuts(query):
    """
    根据关键字查找快捷键
    :param query: 关键字（Id  Name  Accels）
    :return:True or False
    """
    interface = dbus_interface()
    result = interface.SearchShortcuts(query)
    if isinstance(result, dbus.String):
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据不是String:{type(result)}')
        return False


@checkword
def lookupConflictingShortcut(keystroke):
    """
    查找冲突的快捷键
    :param keystroke: 按键组合
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.LookupConflictingShortcut(keystroke)
    if isinstance(result, dbus.String):
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据类型不是String：{type(result)}')
        return False


@checkword
def getShortcut(shortcut_id, shortcut_type):
    """
    获取一个快捷键
    :param shortcut_id:快捷键ID
    :param shortcut_type:快捷键类型
    :return:True or False
    """
    interface = dbus_interface()
    result = interface.GetShortcut(shortcut_id, shortcut_type)
    if isinstance(result, dbus.String):
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据类型不是String：{type(result)}')
        return False


@checkword
def getCapsLockState():
    """
    获取CapsLock的状态
    :return:True or False
    """
    interface = dbus_interface()
    result = interface.GetCapsLockState()
    if isinstance(result, dbus.Int32):
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据类型不是Int32：{type(result)}')
        return False


@checkword
def addCustomShortcut(name, action, keystroke):
    """
    添加一个自定义快捷键
    :param name:快捷键的名字
    :param action:快捷键触发的命令
    :param keystroke:按键组合
    :return:True or False
    """
    interface = dbus_interface()
    result = interface.AddCustomShortcut(name, action, keystroke)
    logging.info(result)
    if isinstance(result[0], dbus.String):
        logging.info(result[0])
        if isinstance(result[1], dbus.Int32):
            logging.info(result[1])
            deleteCustomShortcut(result[0])
            return True
    else:
        logging.info(f'返回数据类型不是Array：{type(result)}')
        return False


@checkword
def deleteCustomShortcut(shortcut_id):
    """
    删除一个自定义快捷键
    :param shortcut_id: 快捷键id
    :return: True or False
    """
    interface = dbus_interface()
    interface.DeleteCustomShortcut(shortcut_id)
    logging.info("检查接口执行成功")
    return True


def getCustomShortcutId(name, action, keystroke):
    """
    添加一个自定义快捷键
    :param name:快捷键的名字
    :param action:快捷键触发的命令
    :param keystroke:按键组合
    :return:自定义快捷键id
    """
    interface = dbus_interface()
    result = interface.AddCustomShortcut(name, action, keystroke)
    logging.info(result)
    shortcut_id = result[0]
    return shortcut_id


@checkword
def modifyCustomShortcut(shortcut_id, new_name, new_action, new_keystroke):
    """
    修改一个自定义快捷键
    :param shortcut_id: 自定义快捷键id
    :param new_name: 新名字
    :param new_action: 新命令
    :param new_keystroke: 新按键组合
    :return: True or False
    """
    interface = dbus_interface()
    interface.ModifyCustomShortcut(shortcut_id, new_name, new_action, new_keystroke)
    logging.info("检查接口执行成功")
    deleteCustomShortcut(shortcut_id)
    logging.info("恢复默认设置")
    return True


@checkword
def deleteShortcutKeystroke(shortcuts_id, shortcuts_type, keystroke):
    """
    删除快捷键的一个按键组合
    :param shortcuts_id: 快捷键的ID
    :param shortcuts_type: 快捷键的类型
    :param keystroke: 要删除的按键组合
    :return: True or False
    """
    interface = dbus_interface()
    interface.DeleteShortcutKeystroke(shortcuts_id, shortcuts_type, keystroke)
    logging.info("检查接口执行成功")
    # reset()
    logging.info("恢复默认设置成功")
    return True


@checkword
def addShortcutKeystroke(shortcuts_id, shortcuts_type, keystroke):
    """
    向一个快捷键中添加一个按键组合
    :param shortcuts_id: 快捷键的id
    :param shortcuts_type: 快捷键的类型，0系统、1自定义、2多媒体、3窗管、4虚拟
    :param keystroke: 按键组合
    :return: True or False
    """
    interface = dbus_interface()
    interface.AddShortcutKeystroke(shortcuts_id, shortcuts_type, keystroke)
    logging.info("检查接口执行成功")
    # reset()
    logging.info("恢复默认设置成功")
    return True


@checkword
def clearShortcutKeystrokes(shortcuts_id, shortcuts_type):
    """
    清除一个快捷键的所以按键组合
    :param shortcuts_id: 快捷键的ID
    :param shortcuts_type: 快捷键的类型
    :return: True or False
    """
    interface = dbus_interface()
    interface.ClearShortcutKeystrokes(shortcuts_id, shortcuts_type)
    logging.info("检查接口执行成功")
    reset()
    logging.info("恢复默认设置成功")
    return True



