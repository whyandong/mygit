# -*- coding: utf-8 -*-
import os
import logging
import dbus

from aw.dbus.dbus_common import get_session_dbus_interface
from aw.dbus.sessionBus import sessionCommon
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.daemon.Appearance'
DBUS_PATH = '/com/deepin/daemon/Appearance'
IFACE_NAME = 'com.deepin.daemon.Appearance'


def dbus_interface():
    return get_session_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


@checkword
def delete(resource, name):
    """
    删除资源，包含主题 图表 光标 背景
    :param resource: 资源类型  包括主题 图表 光标 背景
    :param name: 资源名称
    :return: True or False
    """
    interface = dbus_interface()
    interface.Delete(resource, name)
    logging.info("检查接口执行成功")
    return True


@checkword
def reset():
    """
    重置个性化设置为默认设置参数
    :return:True
    """
    interface = dbus_interface()
    interface.Reset()
    logging.info("检查接口执行成功")
    return True


@checkword
def getList(resource):
    """
    列出所有可用的特殊类型的文件和资源，返回json格式列表
    :param resource: 文件或资源，包含主题 图表 光标 背景 字体等
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.List(dbus.String(resource))
    if isinstance(result, dbus.String):
        logging.info(result)
        return True
    else:
        logging.info(f'返回数据不是list:{type(result)}')
        return False


@checkword
def getScaleFactor():
    """
    获取窗口缩放比例
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.GetScaleFactor()
    if isinstance(result, dbus.Double):
        logging.info(result)
        return True
    else:
        logging.info(f'返回的数据不是Double:{type(result)}')
        return False


@checkword
def getScreenScaleFactors():
    """
    获取屏幕缩放比例,返回字典对象
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.GetScreenScaleFactors()
    if isinstance(result, dbus.Dictionary):
        logging.info(result)
        return True
    else:
        logging.info(f'返回的数据不是字典:{type(result)}')
        return False


def getMonitorName():
    """
    获取当前屏幕名称
    :return: screen_name
    """
    interface = dbus_interface()
    result = interface.GetScreenScaleFactors()
    monitor_name = result.keys()
    return monitor_name


def checkScreenScaleFactors():
    """
    获取当前每个屏幕的缩放比例
    :return: result
    """
    interface = dbus_interface()
    result = interface.GetScreenScaleFactors()
    return result


@checkword
def setScreenScaleFactors(scale_factor):
    """
    设置每个屏幕的缩放比例，和GetScreenScaleFactors对应参数
    :return:True or False
    """
    interface = dbus_interface()
    interface.SetScreenScaleFactors(scale_factor)
    logging.info("检查接口执行成功")
    return True


@checkword
def setWallpaperSlideShow(monitor_name, slide_time):
    """
    根据屏幕名称设置该屏幕桌面壁纸的轮换时间参数
    :return: True or False
    """
    interface = dbus_interface()
    interface.SetWallpaperSlideShow(dbus.String(monitor_name), dbus.String(slide_time))
    logging.info("检查接口执行成功")
    return True


@checkword
def getWallpaperSlideShow(name):
    """
    根据显示器名称获取该显示器壁纸切换间隔,返回String数据类型
    :param name: 显示器名称
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.GetWallpaperSlideShow(dbus.String(name))
    if isinstance(result, dbus.String):
        logging.info(result)
        return True
    else:
        logging.info(f'返回的数据类型不是String:{type(result)}')
        return False


@checkword
def showDetail(resource_name, name_list):
    """
    显示特殊类型的详细信息，返回json格式列表参数
    :return:True or False
    """
    interface = dbus_interface()
    result = interface.Show(resource_name, name_list)
    logging.info(result)
    if isinstance(result, dbus.String):
        logging.info("显示特殊类型的详细信息成功")
        return True
    else:
        logging.info("显示特殊类型的详细信息失败")
        return False


@checkword
def setMonitorBackground(name, file):
    """
    根据显示器名称设置桌面背景参数
    :param name: 显示器名称
    :param file: 需要设置的背景图片
    :return: True or False
    """
    picture_type = ['.jpg', '.bmp']
    if not os.path.exists(file):
        picture_path = os.path.splitext(file)[0]
        for item in picture_type:
            picture_file_path = f"{picture_path}{item}"
            if os.path.exists(picture_file_path):
                file = picture_file_path
                logging.info(f"{file}")
                break
        else:
            logging.info('未找到相关图片')
            raise RuntimeError('未找到相关图片')

    interface = dbus_interface()
    interface.SetMonitorBackground(name, file)
    logging.info("检查接口执行成功")
    return True


@checkword
def getBackground():
    """
    获取当前用户设置的桌面壁纸，返回String类型数据
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Appearance', 'Background')
    logging.info(result)
    if isinstance(result, dbus.String):
        logging.info("获取当前用户设置的桌面壁纸成功")
        return True
    else:
        logging.info("获取当前用户设置的桌面壁纸失败")
        return False


@checkword
def getFontSize():
    """
    获取当前用户设置的字体大小，返回Double类型数据
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Appearance', 'FontSize')
    logging.info(result)
    if isinstance(result, dbus.Double):
        logging.info("获取当前用户设置的字体大小成功")
        return True
    else:
        logging.info("获取当前用户设置的字体大小失败")
        return False


@checkword
def getOpacity():
    """
    获取当前用户设置的窗体透明度，返回Double类型数据
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Appearance', 'Opacity')
    logging.info(result)
    if isinstance(result, dbus.Double):
        logging.info("获取当前用户设置的窗体透明度成功")
        return True
    else:
        logging.info("获取当前用户设置的窗体透明度失败")
        return False


@checkword
def getCursorTheme():
    """
    获取当前用户设置的光标主题，返回String类型数据
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Appearance', 'CursorTheme')
    logging.info(result)
    if isinstance(result, dbus.String):
        logging.info("获取当前用户设置的光标主题成功")
        return True
    else:
        logging.info("获取当前用户设置的光标主题失败")
        return False


@checkword
def getGtkTheme():
    """
    获取当前用户设置的窗体主题，返回String类型数据
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Appearance', 'GtkTheme')
    logging.info(result)
    if isinstance(result, dbus.String):
        logging.info("获取当前用户设置的窗体主题成功")
        return True
    else:
        logging.info("获取当前用户设置的窗体主题失败")
        return False


@checkword
def getIconTheme():
    """
    获取当前用户设置的图标主题，返回String类型数据
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Appearance', 'IconTheme')
    logging.info(result)
    if isinstance(result, dbus.String):
        logging.info("获取当前用户设置的图标主题成功")
        return True
    else:
        logging.info("获取当前用户设置的图标主题失败")
        return False


@checkword
def getMonospaceFont():
    """
    获取当前用户设置的等宽字体，返回String类型数据
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Appearance', 'MonospaceFont')
    logging.info(result)
    if isinstance(result, dbus.String):
        logging.info("获取当前用户设置的等宽字体成功")
        return True
    else:
        logging.info("获取当前用户设置的等宽字体失败")
        return False


@checkword
def getQtActiveColor():
    """
    获取当前用户设置的Qt活动颜色，返回String类型数据
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Appearance', 'QtActiveColor')
    logging.info(result)
    if isinstance(result, dbus.String):
        logging.info("获取当前用户设置的Qt活动颜色成功")
        return True
    else:
        logging.info("获取当前用户设置的Qt活动颜色失败")
        return False


@checkword
def getStandardFont():
    """
    获取当前用户设置的桌面壁纸，返回String类型数据
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Appearance', 'StandardFont')
    logging.info(result)
    if isinstance(result, dbus.String):
        logging.info("获取当前用户设置的桌面壁纸成功")
        return True
    else:
        logging.info("获取当前用户设置的桌面壁纸失败")
        return False


@checkword
def showWallpaperSlideShow():
    """
    获取当前用户设置的显示器壁纸轮换时间，返回String类型数据
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Appearance', 'WallpaperSlideShow')
    logging.info(result)
    if isinstance(result, dbus.String):
        logging.info("获取当前用户设置的显示器壁纸轮换时间成功")
        return True
    else:
        logging.info("获取当前用户设置的显示器壁纸轮换时间失败")
        return False


@checkword
def setType(resource, value):
    """
    根据资源类型设置当前资源,返回无
    :return:True or False
    """
    interface = dbus_interface()
    interface.Set(resource, value)
    logging.info("检查接口执行成功")
    return True


@checkword
def setScaleFactor(scale_factor):
    """
    根据资源类型设置当前资源,返回无
    :return:True or False
    """
    interface = dbus_interface()
    interface.SetScaleFactor(scale_factor)
    logging.info("检查接口执行成功")
    return True


@checkword
def getGtkThumbnail(resource, resource_name):
    """
    获取窗体主题缩略图
    :return:True or False
    """
    interface = dbus_interface()
    result = interface.Thumbnail(resource, resource_name)
    logging.info(result)
    if isinstance(result, dbus.String):
        logging.info("获取窗体主题缩略图成功")
        return True
    else:
        logging.info("获取窗体主题缩略图失败")
        return False


@checkword
def getIconThumbnail(resource, resource_name):
    """
    获取图标主题缩略图
    :return:True or False
    """
    interface = dbus_interface()
    result = interface.Thumbnail(resource, resource_name)
    logging.info(result)
    if isinstance(result, dbus.String):
        logging.info("获取图标主题缩略图成功")
        return True
    else:
        logging.info("获取图标主题缩略图失败")
        return False


@checkword
def getCursorThumbnail(resource, resource_name):
    """
    获取光标主题缩略图
    :return:True or False
    """
    interface = dbus_interface()
    result = interface.Thumbnail(resource, resource_name)
    logging.info(result)
    if isinstance(result, dbus.String):
        logging.info("获取光标主题缩略图成功")
        return True
    else:
        logging.info("获取光标主题缩略图失败")
        return False

