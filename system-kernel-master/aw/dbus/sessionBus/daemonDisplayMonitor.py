import logging

import dbus
import time

from frame.decorator import checkword
from aw.dbus.dbus_common import get_session_dbus_interface
from aw.dbus.sessionBus import daemonDisplay

dbus_name = 'com.deepin.SessionManager'
dbus_path = None
iface_name = 'com.deepin.daemon.Display.Monitor'

try:
    dbus_path = daemonDisplay.get_Monitors()
except Exception as e:
    logging.exception(e)


def dbus_interface():
    return get_session_dbus_interface(dbus_name, dbus_path, iface_name)


def get_properties_value(properties: str):
    property_obj = get_session_dbus_interface(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(iface_name, properties)
    return result


def get_X():
    """
    获取显示器起始坐标x
    """
    result = get_properties_value('X')
    if isinstance(result, dbus.Int16):
        logging.info(f'获取显示器起始坐标x值，值为{result}')
        return result
    else:
        logging.info(f'获取显示器起始坐标x值失败,获取到的返回的类型为{type(result)}')


def get_Y():
    """
    获取显示器起始坐标x
    """
    result = get_properties_value('Y')
    if isinstance(result, dbus.Int16):
        logging.info(f'获取显示器起始坐标Y值，值为{result}')
        return result
    else:
        logging.info(f'获取显示器起始坐标Y值失败,获取到的返回的类型为{type(result)}')


def get_Reflect():
    """
    获取显示器的反射率
    """
    result = get_properties_value('Reflect')
    if isinstance(result, dbus.UInt16):
        logging.info(f'获取当前显示器的反射率，值为{result}')
        return result
    else:
        logging.info(f'获取当前显示反射率失败,获取到的返回的类型为{type(result)}')
        return False


def get_RefreshRate():
    """
    获取显示器刷新率
    """
    result = get_properties_value('RefreshRate')
    if isinstance(result, dbus.Double):
        logging.info(f'获取显示器刷新率，值为{result}')
        return result
    else:
        logging.info(f'获取显示器刷新率失败,获取到的返回的类型为{type(result)}')
        return False


def get_Rotation():
    """
    获取显示器方向管理器
    """
    result = get_properties_value('Rotation')
    if isinstance(result, dbus.UInt16):
        logging.info(f'获取当前显示器的方向，值为{result}')
        return result
    else:
        logging.info(f'获取当前显示方向失败,获取到的返回的类型为{type(result)}')
        return False


"""=================================方法===================================================="""


@checkword
def setPosition(x, y):
    """设置显示器起始坐标值"""
    interface = dbus_interface()
    interface.SetPosition(dbus.Int16(x), dbus.Int16(y))
    time.sleep(1)
    if dbus.Int16(x) == get_X() and dbus.Int16(y) == get_Y():
        logging.info(f'获取到的显示器起始坐标值为{x}，{y}')
        return True
    else:
        logging.info(f'设置显示器的坐标值失败,设置的值为{x},{y},生效的值为{get_X()},{get_Y()}')
        return False


@checkword
def setReflect(value):
    """设置显示器Reflect值"""
    interface = dbus_interface()
    interface.SetReflect(dbus.UInt16(value))
    time.sleep(1)
    if dbus.UInt16(value) == get_Reflect():
        logging.info(f'设置显示器Reflect值成功，为{value}')
        return True
    else:
        logging.info(f'设置显示器的坐标值失败,设置的值为{value},生效的值为{get_Reflect()}')
        return False


@checkword
def setRefreshRate(value):
    """设置显示器刷新率"""
    interface = dbus_interface()
    interface.SetRefreshRate(dbus.Double(value))
    time.sleep(1)
    if dbus.Double(value) == get_RefreshRate():
        logging.info(f'设置显示器刷新率成功，为{value}')
        return True
    else:
        logging.info(f'设置显示器刷新率失败,设置的值为{value},生效的值为{get_RefreshRate()}')
        return False


@checkword
def setRotation(value):
    """设置显示器Rotation"""
    interface = dbus_interface()
    interface.SetRotation(dbus.UInt16(value))
    time.sleep(1)
    if dbus.UInt16(value) == get_Rotation():
        logging.info(f'设置显示器Rotation成功，为{value}')
        return True
    else:
        logging.info(f'设置显示器Rotation失败,设置的值为{value},生效的值为{get_RefreshRate()}')
        return False


'''=================================属性====================================================='''


@checkword
def getModes():
    """
    获取显示器模式信息
    """
    result = get_properties_value('Modes')
    if isinstance(result, dbus.Array):
        logging.info(f'获取模式成功')
        return True
    else:
        logging.info(f'获取模失败,获取到的结果的类型为{type(result)}')
        return False


@checkword
def getPreferredModes():
    """
    获取显示器模式信息
    """
    result = get_properties_value('PreferredModes')
    if isinstance(result, dbus.Array):
        logging.info(f'获取偏好模式成功')
        return True
    else:
        logging.info(f'获取偏好模式失败,获取到的显示模式的类型为{type(result)}')
        return False


@checkword
def getReflects():
    """
    获取显示器Reflects信息
    """
    result = get_properties_value('Reflects')
    if isinstance(result, dbus.Array):
        logging.info(f'获取显示器反射值式成功')
        return True
    else:
        logging.info(f'获取显示器反射模式失败,获取到的返回的类型为{type(result)}')
        return False


@checkword
def getRotations():
    """
    获取显示器旋转信息
    """
    result = get_properties_value('Rotations')
    if isinstance(result, dbus.Array):
        logging.info(f'获取显示器旋转方向式成功')
        return True
    else:
        logging.info(f'获取显示器旋转方向失败,获取到的返回的类型为{type(result)}')
        return False


@checkword
def getConnected():
    """
    获取显示器是否已连接
    """
    result = get_properties_value('Connected')
    if isinstance(result, dbus.Boolean):
        logging.info(f'获取显示器是否连接')
        return True
    else:
        logging.info(f'获取显示器连接信息失败,获取到的返回的类型为{type(result)}')
        return False


@checkword
def getEnabled():
    """
    获取显示器是否已开启
    """
    result = get_properties_value('Enabled')
    if isinstance(result, dbus.Boolean):
        logging.info(f'获取显示器是否已开启')
        return True
    else:
        logging.info(f'获取显示器是否已开启,获取到的返回的类型为{type(result)}')
        return False


@checkword
def getRefreshRate():
    """
    获取显示器刷新率
    """
    result = get_properties_value('RefreshRate')
    if isinstance(result, dbus.Double):
        logging.info(f'获取显示器刷新率，值为{result}')
        return True
    else:
        logging.info(f'获取显示器刷新率失败,获取到的返回的类型为{type(result)}')
        return False


@checkword
def getX():
    """
    获取显示器起始坐标x
    """
    result = get_properties_value('X')
    if isinstance(result, dbus.Int16):
        logging.info(f'获取显示器起始坐标x值，值为{result}')
        return True
    else:
        logging.info(f'获取显示器起始坐标x值失败,获取到的返回的类型为{type(result)}')
        return False


@checkword
def getY():
    """
    获取显示器起始坐标x
    """
    result = get_properties_value('Y')
    if isinstance(result, dbus.Int16):
        logging.info(f'获取显示器起始坐标Y值，值为{result}')
        return True
    else:
        logging.info(f'获取显示器起始坐标Y值失败,获取到的返回的类型为{type(result)}')
        return False


@checkword
def getManufacturer():
    """
    获取显示器制造商信息
    """
    result = get_properties_value('Manufacturer')
    if isinstance(result, dbus.String):
        logging.info(f'获取显示器制造商，值为{result}')
        return True
    else:
        logging.info(f'获取显示器制造商失败,获取到的返回的类型为{type(result)}')
        return False


@checkword
def getModel():
    """
    获取显示器型号
    """
    result = get_properties_value('Manufacturer')
    if isinstance(result, dbus.String):
        logging.info(f'获取显示器型号，值为{result}')
        return True
    else:
        logging.info(f'获取显示器型号失败,获取到的返回的类型为{type(result)}')
        return False


@checkword
def getName():
    """
    获取显示器名称
    """
    result = get_properties_value('Name')
    if isinstance(result, dbus.String):
        logging.info(f'获取显示器名称，值为{result}')
        return True
    else:
        logging.info(f'获取显示器名称失败,获取到的返回的类型为{type(result)}')
        return False


@checkword
def getBestMode():
    """
    获取显示器最佳显示模式
    """
    result = get_properties_value('BestMode')
    if isinstance(result, dbus.Struct):
        logging.info(f'获取最佳显示模式，值为{result}')
        return True
    else:
        logging.info(f'获取最佳显示模式失败,获取到的返回的类型为{type(result)}')
        return False


@checkword
def getCurrentMode():
    """
    获取显示器当前显示模式
    """
    result = get_properties_value('CurrentMode')
    if isinstance(result, dbus.Struct):
        logging.info(f'获取当前显示模式，值为{result}')
        return True
    else:
        logging.info(f'获取当前显示模式失败,获取到的返回的类型为{type(result)}')
        return False


@checkword
def getHeight():
    """
    获取显示模式的高
    """
    result = get_properties_value('Height')
    if isinstance(result, dbus.UInt16):
        logging.info(f'获取当前显示模式高，值为{result}')
        return True
    else:
        logging.info(f'获取当前显示高度失败,获取到的返回的类型为{type(result)}')
        return False


@checkword
def getReflect():
    """
    获取显示器的反射率
    """
    result = get_properties_value('Reflect')
    if isinstance(result, dbus.UInt16):
        logging.info(f'获取当前显示器的反射率，值为{result}')
        return True
    else:
        logging.info(f'获取当前显示反射率失败,获取到的返回的类型为{type(result)}')
        return False


@checkword
def getRotation():
    """
    获取显示器方向管理器
    """
    result = get_properties_value('Rotation')
    if isinstance(result, dbus.UInt16):
        logging.info(f'获取当前显示器的方向，值为{result}')
        return True
    else:
        logging.info(f'获取当前显示方向失败,获取到的返回的类型为{type(result)}')
        return False


@checkword
def getWidth():
    """
    获取显示器方向管理器
    """
    result = get_properties_value('Width')
    if isinstance(result, dbus.UInt16):
        logging.info(f'获取当前显示器的宽度，值为{result}')
        return True
    else:
        logging.info(f'获取当前显示器宽度失败,获取到的返回的类型为{type(result)}')
        return False


@checkword
def getID():
    """
    获取显示器方向管理器
    """
    result = get_properties_value('ID')
    if isinstance(result, dbus.UInt32):
        logging.info(f'获取当前显示器的ID路径，值为{result}')
        return True
    else:
        logging.info(f'获取当前显示器ID路径失败,获取到的返回的类型为{type(result)}')
        return False


@checkword
def getMmHeight():
    """
    获取显示器的mmheight
    """
    result = get_properties_value('MmHeight')
    if isinstance(result, dbus.UInt32):
        logging.info(f'获取当前显示器的MmHeight，值为{result}')
        return True
    else:
        logging.info(f'获取当前显示器MmHeight失败,获取到的返回的类型为{type(result)}')
        return False


@checkword
def getMmWidth():
    """
    获取显示器的mmWidth
    """
    result = get_properties_value('MmWidth')
    if isinstance(result, dbus.UInt32):
        logging.info(f'获取当前显示器的MmWidth，值为{result}')
        return True
    else:
        logging.info(f'获取当前显示器MmWidth失败,获取到的返回的类型为{type(result)}')
        return False

@checkword
def getAvailableFillModes():
    """
    通过xrandr --prop指令，不同显示器下scaling mode下的supported类型，[]string输出
    """
    result = get_properties_value('AvailableFillModes')
    if isinstance(result, dbus.Array):
        logging.info(f'获取当前显示器不同显示器下scaling mode下的supported类型，[]string输出，值为{result}')
        return True
    else:
        logging.info(f'获取当前显示器AvailableFillModes失败,获取到的返回的类型为{type(result)}')
        return False

@checkword
def getCurrentFillMode():
    """
    通过~/.config/deepin/startdde/display_v5.json配置文件中，此屏幕的uuid和当前分辨率提取当前的铺满方式，并输出；
    同时startdde通过此属性set回调监听，设置想要设置的铺满方式，并写入配置文件
    """
    result = get_properties_value('CurrentFillMode')
    if isinstance(result, dbus.String):
        logging.info(f'获取当前显示器CurrentFillMode，值为{result}')
        return True
    else:
        logging.info(f'获取当前显示器CurrentFillMode失败,获取到的返回的类型为{type(result)}')
        return False