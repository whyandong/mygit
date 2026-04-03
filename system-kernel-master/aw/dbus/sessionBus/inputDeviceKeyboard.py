# -*- coding: utf-8 -*-
import time
import logging

import dbus

from frame.decorator import checkword
from aw.dbus.dbus_common import get_session_dbus_interface

DBUS_NAME = 'com.deepin.daemon.InputDevices'
DBUS_PATH = '/com/deepin/daemon/InputDevice/Keyboard'
IFACE_NAME = 'com.deepin.daemon.InputDevice.Keyboard'


def dbus_interface():
    return get_session_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


def get_properties_value(properties: str):
    property_obj = get_session_dbus_interface(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(IFACE_NAME, properties)
    return result


def get_layout_list():
    """
    获取 layout list
    :return: list
    """
    interface = dbus_interface()
    result = interface.LayoutList()
    if isinstance(result, dbus.Dictionary):
        layouts_list = [str(key) for key in result]
        logging.info(f'user layouts:{layouts_list}')
        return layouts_list
    else:
        raise RuntimeError("未能正确获取layout list")


def get_layout_options() -> dbus.Array:
    """
    读取 UserOptionList 属性
    :return: dbus.Array
    """
    result = get_properties_value('UserOptionList')
    if isinstance(result, dbus.Array):
        logging.info(f'options:{result}')
        return result
    else:
        logging.info(f'数据类型不正确，result：{type(result)}')
        raise RuntimeError(f'数据类型不正确，result：{type(result)}')


def clear_layout_options():
    """
    clear layout option
    :return: None
    """
    logging.info(f"clear layout option")
    interface = dbus_interface()
    interface.ClearLayoutOption()


def get_user_layouts() -> dbus.Array:
    """
    读取 UserLayoutList 属性
    :return: dbus.Array
    """
    result = get_properties_value('UserLayoutList')
    if isinstance(result, dbus.Array):
        logging.info(f'user layouts:{result}')
        return result
    else:
        logging.info(f'数据类型不正确，result：{type(result)}')
        raise RuntimeError(f'数据类型不正确，result：{type(result)}')


def delete_user_layout(layout):
    """
    delete user layout
    :param layout: 待删除的键盘布局
    :return: None
    """
    logging.info(f"delete user layout: {layout}")
    interface = dbus_interface()
    interface.DeleteUserLayout(dbus.String(layout))


def clear_user_layouts():
    """
    clear user layout
    :return: None
    """
    logging.info(f"clear user layout")
    layouts = get_user_layouts()
    if layouts:
        for item in layouts:
            delete_user_layout(item)
    else:
        logging.info("layouts is None")


def check_add_layout_option(option):
    """
    检查添加键盘布局选项是否成功
    :param option: 待添加的键盘布局选项
    :return: True or False
    """
    options = get_layout_options()
    return dbus.String(option) in options


def check_add_user_layout(layout):
    """
    检查添加用户键盘布局是否成功
    :param layout: 待添加的键盘布局
    :return: True or False
    """
    layouts = get_user_layouts()
    return dbus.String(layout) in layouts


def check_clear_layout_option():
    """
    检查清除键盘布局选项是否成功
    :return: True or False
    """
    options = get_layout_options()
    if options:
        return False
    else:
        return True


def check_delete_layout_option(option):
    """
    检查删除键盘布局选项是否成功
    :param option:键盘布局选项
    :return: True or False
    """
    options = get_layout_options()
    return dbus.String(option) not in options


def check_delete_user_layout(layout):
    """
    检查删除用户键盘布局使用成功
    :param layout: 键盘布局
    :return: True or False
    """
    layouts = get_user_layouts()
    return dbus.String(layout) not in layouts


"""
=========================功能函数=================================
=========================接口方法=================================
"""


@checkword
def addLayoutOption(option):
    """
    AddLayoutOption(string option) -> (),增加键盘布局选项
    参数 option : 键盘布局选项
    :param option: 任意字符串
    :return: True or False
    """
    logging.info(f"添加键盘布局{option}")
    interface = dbus_interface()
    interface.AddLayoutOption(option)
    time.sleep(2)
    add_result = check_add_layout_option(option)
    logging.info(f"添加键盘布局{option}:{add_result}")
    return add_result


@checkword
def addUserLayout(layout, err=False):
    """
    AddUserLayout(string layout) -> (),增加用户键盘布局
    参数 layout: 键盘布局
    :param layout: 'cn;' or 'cn;altgr-pinyin',目前只有这两种布局，可以通过LayoutList获取，传入不存在的布局会引发‘invalid layout’错误
    :param err: 是否引发‘invalid layout’错误
    :return: True or False
    """
    logging.info(f"添加键盘布局{layout}")
    interface = dbus_interface()
    if err:
        err_name = 'invalid layout'
        try:
            logging.info(f"预期引发{err_name}错误")
            interface.AddUserLayout(layout)
            logging.info(f"未成功引发{err_name}")
            return False
        except dbus.DBusException as e:
            if 'invalid layout' in e.get_dbus_message():
                logging.info(f"成功引发{err_name}")
                return True
            else:
                logging.info(f"引发的错误与预期不符合：{err_name}")
                return False
    else:
        interface.AddUserLayout(layout)
        time.sleep(2)
        add_result = check_add_user_layout(layout)
        logging.info(f"添加键盘布局{layout}:{add_result}")
        return add_result


@checkword
def clearLayoutOption():
    """
    ClearLayoutOption() -> (),清空键盘布局选项
    :return: True or False
    """
    interface = dbus_interface()
    interface.ClearLayoutOption()
    time.sleep(2)
    clear_result = check_clear_layout_option()
    logging.info(f'clear_result: {clear_result}')
    return clear_result


@checkword
def deleteLayoutOption(option):
    """
    DeleteLayoutOption(string option) -> (),删除一个键盘布局选项
    参数 option: 键盘布局选项
    :return: True or False
    """
    logging.info(f"删除键盘布局{option}")
    interface = dbus_interface()
    interface.DeleteLayoutOption(option)
    time.sleep(2)
    delete_result = check_delete_layout_option(option)
    logging.info(f'delete_result: {delete_result}')
    return delete_result


@checkword
def deleteUserLayout(layout):
    """
    DeleteUserLayout(string layout) -> (),删除一个用户键盘布局
    参数  layout : 键盘布局
    :return: True or False
    """
    logging.info(f"删除键盘布局{layout}")
    interface = dbus_interface()
    interface.DeleteUserLayout(layout)
    time.sleep(2)
    delete_result = check_delete_user_layout(layout)
    if delete_result:
        logging.info(f"删除{layout}布局成功")
    else:
        logging.info(f"删除{layout}布局失败")
    return delete_result


@checkword
def getLayoutDesc(layout):
    """
    GetLayoutDesc(string layout) -> (string description),获取键盘布局的说明
    参数 layout : 键盘布局
    返回值 description : 说明
    :return: True or False
    """
    logging.info(f"获取键盘布局{layout}的说明")
    interface = dbus_interface()
    result = interface.GetLayoutDesc(layout)
    if isinstance(result, dbus.String):
        logging.info(f"说明: {result}")
        return True
    else:
        logging.info(f"GetLayoutDesc返回的数据类型不是预期的bus.String，实际类型为{type(result)}")
        return False


@checkword
def layoutList():
    """
    LayoutList() -> (map[string]string layout_list),获取键盘布局列表
    返回值 layout_list : 键盘布局列表
    :return: True or False
    """
    logging.info(f"获取键盘布局列表")
    interface = dbus_interface()
    result = interface.LayoutList()
    if isinstance(result, dbus.Dictionary):
        logging.info(f"键盘布局列表: {dict(result)}")
        return True
    else:
        logging.info(f"GetLayoutDesc返回的数据类型不是预期的dbus.Dictionary，实际类型为{type(result)}")
        return False


@checkword
def reset():
    """
    Reset() -> ()
    重置
    :return: True
    """
    logging.info(f"重置")
    interface = dbus_interface()
    interface.Reset()
    return True


"""
=========================接口方法=================================
=========================接口属性=================================
"""


def userOptionList():
    """
    as UserOptionList (read) 用户选项列表
    :return: True or False
    """
    result = get_properties_value('UserOptionList')
    if isinstance(result, dbus.Array):
        logging.info(f"用户选项列表: {result}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
        return False


def cursorBlink():
    """
    int32 CursorBlink (readwrite),光标闪烁速度
    :return: True or False
    """
    result = get_properties_value('CursorBlink')
    if isinstance(result, dbus.Int32):
        logging.info(f"光标闪烁速度: {result}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
        return False


def repeatInterval():
    """
    uint32 RepeatInterval (readwrite) 长按时每隔多久重复一次
    :return: True or False
    """
    result = get_properties_value('RepeatInterval')
    if isinstance(result, dbus.UInt32):
        logging.info(f"长按时每隔多久重复一次: {result}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
        return False


def layoutScope():
    """
    int32 LayoutScope (readwrite),布局有效范围，0全局,1应用
    :return: True or False
    """
    result = get_properties_value('LayoutScope')
    if isinstance(result, dbus.Int32):
        logging.info(f"布局有效范围，0全局,1应用: {result}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
        return False


def userLayoutList():
    """
    as UserLayoutList (read),当前用户键盘布局列表
    :return: True or False
    """
    result = get_properties_value('UserLayoutList')
    if isinstance(result, dbus.Array):
        logging.info(f"当前用户键盘布局列表: {result}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
        return False


def repeatEnabled():
    """
    bool RepeatEnabled (readwrite),是否重复
    :return: True or False
    """
    result = get_properties_value('RepeatEnabled')
    if isinstance(result, dbus.Boolean):
        logging.info(f"是否重复: {bool(result)}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
        return False


def currentLayout():
    """
    string CurrentLayout (readwrite),当前键盘布局
    :return: True or False
    """
    result = get_properties_value('CurrentLayout')
    if isinstance(result, dbus.String):
        logging.info(f"当前键盘布局: {result}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
        return False


def capslockToggle():
    """
    bool CapslockToggle (readwrite),切换Caplock时是否显示OSD
    :return: True or False
    """
    result = get_properties_value('CapslockToggle')
    if isinstance(result, dbus.Boolean):
        logging.info(f"是否重复: {bool(result)}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
        return False


def repeatDelay():
    """
    uint32 RepeatDelay (readwrite),长按时延迟多久开始重复
    :return: True or False
    """
    result = get_properties_value('RepeatDelay')
    if isinstance(result, dbus.UInt32):
        logging.info(f"是否重复: {result}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
        return False
