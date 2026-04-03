# -*- coding:utf-8 -*-
import dbus
import logging

from aw.dbus.dbus_common import get_session_dbus_interface

DBUS_NAME = 'com.deepin.daemon.InputDevices'
DBUS_PATH = '/com/deepin/daemon/InputDevice/Wacom'
IFACE_NAME = 'com.deepin.daemon.InputDevice.Wacom'


def dbus_interface():
    return get_session_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


def get_properties_value(properties: str):
    property_obj = get_session_dbus_interface(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(IFACE_NAME, properties)
    return result


def reset():
    """
    Reset() -> ()
    重置
    :return: True
    """
    interface = dbus_interface()
    interface.Reset()
    return True


def actionInfos():
    """
    InfoStruct[] ActionInfos (read)
    type InfoStruct struct {
      string Action
      string Desc
    }
    信息列表
    字段含义:
            Action : 响应
            Desc : 描述说明
    :return: True or False
    """
    result = get_properties_value(dbus.String('ActionInfos'))
    if isinstance(result, dbus.Array):
        if result:
            for action_info in result:
                if isinstance(action_info, dbus.Struct):
                    logging.info(action_info)  # 需要有设备再做测试编写判断逻辑
                else:
                    return False
        return True
    else:
        logging.info('返回数据类型不匹配')
        logging.info(f'返回数据类型为：{type(result)}')
        return False


def mouseEnterRemap() -> bool:
    """
    bool MouseEnterRemap(readwrite)
    当属性为True时，开启鼠标自动映射，意味着，当鼠标移动到新屏幕的时候，当在新屏幕启用画笔时，此时实际操作的为当前控制板
    当属性为False时，关闭鼠标映射，当在扩展板操作时，鼠标自动映射到主显示屏的相应位置
    :return:True or False
    """
    result = get_properties_value(dbus.String('MouseEnterRemap'))
    if isinstance(result, dbus.Boolean):
        logging.info(f'MouseEnterRemap:{result}')
        return True
    else:
        logging.info('返回数据类型不匹配')
        return False


def deviceList() -> bool:
    """
    string DeviceList (read)
    设备列表
    :return:string
    """
    result = get_properties_value(dbus.String('DeviceList'))
    if isinstance(result, dbus.String):
        logging.info(f'DeviceList:{result}')
        return True
    else:
        logging.info('返回数据类型不匹配')
        return False


def leftHanded() -> bool:
    """
    bool LeftHanded (readwrite)
    是否使用左手模式
    :return:True or False
    """
    result = get_properties_value(dbus.String('LeftHanded'))
    if isinstance(result, dbus.Boolean):
        logging.info(f'LeftHanded:{result}')
        return True
    else:
        logging.info('返回数据类型不匹配')
        return False


def stylusThreshold() -> bool:
    """
    uint32 StylusThreshold (readwrite)
    触笔阈值
    :return:uint32
    """
    result = get_properties_value(dbus.String('StylusThreshold'))
    if isinstance(result, dbus.UInt32):
        logging.info(f'StylusThreshold:{result}')
        return True
    else:
        logging.info('返回数据类型不匹配')
        return False


def eraserThreshold() -> bool:
    """
    uint32 EraserThreshold (readwrite)
    擦除阈值
    :return:uint32
    """
    result = get_properties_value(dbus.String('EraserThreshold'))
    if isinstance(result, dbus.UInt32):
        logging.info(f'EraserThreshold:{result}')
        return True
    else:
        logging.info('返回数据类型不匹配')
        return False


def forceProportions() -> bool:
    """
    bool ForceProportions (readwrite)
    是否强制粗细均匀
    :return:True or False
    """
    result = get_properties_value(dbus.String('ForceProportions'))
    if isinstance(result, dbus.Boolean):
        logging.info(f'ForceProportions:{result}')
        return True
    else:
        logging.info('返回数据类型不匹配')
        return False


def keyDownAction() -> bool:
    """
    string KeyDownAction (readwrite)
    下键触发的动作
    :return:string
    """
    result = get_properties_value(dbus.String('KeyDownAction'))
    if isinstance(result, dbus.String):
        logging.info(f'KeyDownAction:{result}')
        return True
    else:
        logging.info('返回数据类型不匹配')
        return False


def suppress() -> bool:
    """
    uint32 Suppress (readwrite)
    变化量抑制等级，xy坐标变化大于这个值才有效，取值0～100
    :return:uint32
    """
    result = get_properties_value(dbus.String('Suppress'))
    if isinstance(result, dbus.UInt32):
        logging.info(f'Suppress:{result}')
        if 0 <= int(result) <= 100:
            return True
        else:
            logging.info('数据超出界限0-100')
            return False
    else:
        logging.info('返回数据类型不匹配')
        return False


def eraserRawSample() -> bool:
    """
    uint32 EraserRawSample (readwrite)
    擦除模式滑动采样窗口
    :return:uint32
    """
    result = get_properties_value(dbus.String('EraserRawSample'))
    if isinstance(result, dbus.UInt32):
        logging.info(f'EraserRawSample:{result}')
        return True
    else:
        logging.info('返回数据类型不匹配')
        return False


def exist() -> bool:
    """
    bool Exist (read)
    是否存在
    :return:True or False
    """
    result = get_properties_value(dbus.String('Exist'))
    if isinstance(result, dbus.Boolean):
        logging.info(f'Exist:{result}')
        return True
    else:
        logging.info('返回数据类型不匹配')
        return False


def keyUpAction() -> bool:
    """
    string KeyUpAction (readwrite)
    上键触发的动作
    :return:string
    """
    result = get_properties_value(dbus.String('KeyUpAction'))
    if isinstance(result, dbus.String):
        logging.info(f'KeyUpAction:{result}')
        return True
    else:
        logging.info('返回数据类型不匹配')
        return False


def mapOutput() -> bool:
    """
    string MapOutput (read)
    映射的显示器
    需要相关外设支持
    :return:string
    """
    result = get_properties_value(dbus.String('MapOutput'))
    if isinstance(result, dbus.String):
        logging.info(f'MapOutput:{result}')
        return True
    else:
        logging.info('返回数据类型不匹配')
        return False


def cursorMode() -> bool:
    """
    bool CursorMode (readwrite)
    光标模式，true相对模式(光标根据数位笔坐标变化量移动)，false绝对模式（光标跟随数位笔的绝对坐标）
    :return:True or False
    """
    result = get_properties_value(dbus.String('CursorMode'))
    if isinstance(result, dbus.Boolean):
        logging.info(f'CursorMode:{result}')
        return True
    else:
        logging.info('返回数据类型不匹配')
        return False


def stylusPressureSensitive() -> bool:
    """
    uint32 StylusPressureSensitive (readwrite)
    触笔灵敏度
    :return:uint32
    """
    result = get_properties_value(dbus.String('StylusPressureSensitive'))
    if isinstance(result, dbus.UInt32):
        logging.info(f'StylusPressureSensitive:{result}')
        return True
    else:
        logging.info('返回数据类型不匹配')
        return False


def eraserPressureSensitive() -> bool:
    """
    uint32 EraserPressureSensitive (readwrite)
    触笔灵敏度
    :return:uint32
    """
    result = get_properties_value(dbus.String('StylusPressureSensitive'))
    if isinstance(result, dbus.UInt32):
        logging.info(f'StylusPressureSensitive:{result}')
        return True
    else:
        logging.info('返回数据类型不匹配')
        return False
