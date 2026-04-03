# -*- coding: utf-8 -*-
import logging
import dbus
import time

from frame.decorator import checkword
from aw.dbus.systemBus import systemCommon
from aw.dbus.dbus_common import get_system_dbus_interface

DBUS_NAME = 'com.deepin.daemon.Uadp'
DBUS_PATH = '/com/deepin/daemon/Uadp'
IFACE_NAME = 'com.deepin.daemon.Uadp'


def dbus_interface():
    return get_system_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


def get_properties_value(properties: str):
    property_obj = get_system_dbus_interface(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(IFACE_NAME, properties)
    return result


@checkword
def available():
    """
    判断此服务是否可用
    :param mode:None
    :return:None
    """
    interface = dbus_interface()
    result = interface.Available()
    logging.info(f'Uadp服务可用状态:{result}')
    if isinstance(result, dbus.Boolean):
        return True
    else:
        logging.info(f'Uadp服务可用状态返回值类型错误，类型为:{type(result)}')
        return False

@checkword
def delete(name):
    """
    删除加密数据
    :param name:String 加密数据名称
    :return:None
    """
    interface = dbus_interface()
    interface.Delete(dbus.String(name))
    logging.info(f'删除数据加密数据名称为:{name}')
    return True

@checkword
def get(name):
    """
    通过名称获取加密数据内容
    :param name:String 加密数据名称
    :return Array:list 数字列表
    """
    interface = dbus_interface()
    result = interface.Get(dbus.String(name))
    logging.info(f'加密数据为:{result}')
    if isinstance(result,dbus.Array):
        return True
    else:
        logging.info(f'Uadp服务可用状态返回值类型错误，类型为:{type(result)}')
        return False

def get_Get(name):
    """
    通过名称获取加密数据内容
    :param name:String 加密数据名称
    :return Array:list 数字列表
    """
    interface = dbus_interface()
    result = interface.Get(dbus.String(name))
    logging.info(f'{name}的加密数据为:{result}')
    return result

@checkword
def listname():
    """
    列出所有加密数据的名字
    :param:None
    :return:None
    """
    interface = dbus_interface()
    result = interface.ListName()
    logging.info(f'加密数据名称为:{result}')
    if isinstance(result,dbus.Array):
        return True
    else:
        logging.info(f'加密名称返回值类型错误，类型为:{type(result)}')
        return False

@checkword
def release():
    """
    清空所有加密数据
    :param None:
    :return:None
    """
    interface = dbus_interface()
    interface.Release()
    logging.info(f'清空数据加密数据')
    return True

@checkword
def set(name,data):
    """
    设置加密名称和加密数据
    :param:name Srting
    :param:data Array
    """
    interface = dbus_interface()
    interface.Set(dbus.String(name),data)
    return True

@checkword
def check_vaule(name,data):
    """
    检查设置的加密数据是否正确设置
    :param:name 加密数据名称
    :param:data 加密数据
    """
    interface = dbus_interface()
    result = interface.Get(name)
    if data[0] in result:
        return True
    else:
        logging.info(f'检查点失败,获取到的值为{result},待验证的值{data}')
        return False

@checkword
def check_name(name):
    """
    检查设置的加密数据是否正确设置
    :param:name 加密数据名称
    :param:data 加密数据
    """
    interface = dbus_interface()
    result = interface.ListName()
    if name in result:
        return True
    else:
        logging.info(f'检查点失败,获取到的值为{result},待验证的值{name}')
        return False

@checkword
def check_delete_vaule(name):
    """
        检查设置的加密数据是否正确设置
        :param:name 加密数据名称
        """
    interface = dbus_interface()
    result = interface.ListName()
    if name not in result:
        return True
    else:
        logging.info(f'检查点失败,获取到的值为{result},待验证的值{name}')
        return False




if __name__ == '__main__':
    available()
