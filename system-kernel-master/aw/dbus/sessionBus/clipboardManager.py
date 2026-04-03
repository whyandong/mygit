# -*- coding: utf-8 -*-
import logging
import dbus

from aw.dbus.dbus_common import get_session_dbus_interface
from aw.dbus.sessionBus import sessionCommon
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.daemon.ClipboardManager'
DBUS_PATH = '/com/deepin/daemon/ClipboardManager'
IFACE_NAME = 'com.deepin.daemon.ClipboardManager'


def dbus_interface():
    return get_session_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


@checkword
def becomeClipboardOwner():
    """
    设置当前剪切板所有者
    :return: True or False
    """
    interface = dbus_interface()
    interface.BecomeClipboardOwner()
    logging.info("检查接口执行成功")
    return True


@checkword
def removeTarget(target):
    """
    移除剪切板上指定信息
    :param target: 剪切板上的数据标识， 标识相对应数据信息
    :return: True or False
    """
    interface = dbus_interface()
    interface.RemoveTarget(target)
    logging.info("检查接口执行成功")
    return True


@checkword
def saveClipboard():
    """
    保存剪切板数据
    :return: True or False
    """
    interface = dbus_interface()
    interface.SaveClipboard()
    logging.info("检查接口执行成功")
    return True


@checkword
def writeContent():
    """
    将剪切板内容写进文件(文件保存目录： /tmp/dde-session-daemon-clipboard）
    :return: True or False
    """
    interface = dbus_interface()
    interface.WriteContent()
    logging.info("检查接口执行成功")
    return True
