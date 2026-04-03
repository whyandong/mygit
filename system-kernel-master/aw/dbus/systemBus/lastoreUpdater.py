# -*- coding: utf-8 -*-
import time
import logging

import dbus

from aw.dbus.systemBus import systemCommon
from frame.decorator import checkword

dbus_name = 'com.deepin.lastore'
dbus_path = '/com/deepin/lastore'
iface_name = 'com.deepin.lastore.Updater'


def getPropertiesValue(properties: str):
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(iface_name, properties)
    return result


def listMirrorSources(lang: str = "zh_CN") -> bool:
    """
    ListMirrorSources：获取镜像源
    :param lang: 语言代号，默认使用简体中文'zh_CN'
    :return: True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    mirror_sources_list_info = property_obj.ListMirrorSources(dbus.String(lang))
    for info in mirror_sources_list_info:
        logging.info(info)
        if dbus.String('http://cdn.packages.deepin.com/deepin/') in info:  # 判断官方源是否在列表中
            logging.info('获取到了官方默认源')
            return True
    else:
        return False


def getCheckIntervalAndTime() -> bool:
    """
    GetCheckIntervalAndTime：获取检查周期和最新的检查时间
                             在设置中心->更新->检查更新，点击重新检查更新会刷新最新的检查时间
    :return: True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    interval, check_time = property_obj.GetCheckIntervalAndTime()
    logging.info(f'interval:{interval}\ncheckTime:{check_time}')
    try:
        # 尝试将字符串转化为 struct_time
        time_struct = time.strptime(str(check_time).split('.')[0], "%Y-%m-%d %H:%M:%S")
        logging.info(f'时间转换成功:{time_struct}')
        return True
    except Exception as e:
        logging.error(e)
        logging.info('时间转换失败')
        return False


def applicationUpdateInfos(lang: str = "zh_CN") -> bool:
    """
    ApplicationUpdateInfos:获取应用程序更新信息,对应应用商店->应用更新中的信息
    :param lang: 语言代号，默认使用简体中文'zh_CN'
    :return: True
    """

    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    application_update_infos = property_obj.ApplicationUpdateInfos(dbus.String(lang))
    if application_update_infos:
        for info in application_update_infos:
            logging.info(f'软件名：{info[1]}；包名：{info[2]}；当前版本：{info[3]}；最新版本：{info[4]}')
    else:
        logging.info(f'暂无可更新软件')
    return True


def setAutoCheckUpdates(target: bool = True) -> bool:
    """
    SetAutoCheckUpdates:设置是否自动检查更新,对应设置中心->更新->更新设置—>检查更新
    :param target:True or False
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    property_obj.SetAutoCheckUpdates(dbus.Boolean(target))
    result = getPropertiesValue(dbus.String('AutoCheckUpdates'))
    logging.info(f'AutoCheckUpdates:{result}')
    if result == dbus.Boolean(target):
        logging.info(f'AutoCheckUpdates设置为 {target} 成功')
        return True
    else:
        logging.info(f'AutoCheckUpdates设置为 {target} 失败')
        return False


def setAutoDownloadUpdates(target: bool = True) -> bool:
    """
    SetAutoDownloadUpdates:设置是否自动下载更新
                            设置为True，设置中心->更新->检查更新将自动下载补丁包，打开设置中心->更新->更新设置—>更新提醒
                           可以看到下载更新按钮，其状态对应AutoDownloadUpdates值
    :param target:True or False
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    property_obj.SetAutoDownloadUpdates(dbus.Boolean(target))
    result = getPropertiesValue(dbus.String('AutoDownloadUpdates'))
    logging.info(f'AutoDownloadUpdates:{result}')
    if result == dbus.Boolean(target):
        logging.info(f'AutoDownloadUpdates设置为 {target} 成功')
        return True
    else:
        logging.info(f'AutoDownloadUpdates设置为 {target} 失败')
        return False


def setUpdateNotify(target: bool = True) -> bool:
    """
    SetUpdateNotify:设置是否通知更新。,对应设置中心->更新->更新设置—>更新提醒
    :param target:True or False
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    property_obj.SetUpdateNotify(dbus.Boolean(target))
    result = getPropertiesValue(dbus.String('UpdateNotify'))
    logging.info(f'UpdateNotify:{result}')
    if result == dbus.Boolean(target):
        logging.info(f'UpdateNotify设置为 {target} 成功')
        return True
    else:
        logging.info(f'UpdateNotify设置为 {target} 失败')
        return False


def set_mirror_source(passwd, source_id: str = "Aliyun"):
    """
    SetMirrorSource:将id添加到用于下载软件的镜像源，如果添加失败，则会恢复之前的镜像源。
                    注意这里是设置中心系统更新源，不是/etc/apt/sources.list中的内容
    :param passwd:密码,修改/etc/apt/apt.conf.d/99mirrors.conf需要管理源权限
    :param source_id:调用ListMirrorSources会返回所有可用源
    :return: None
    """
    dbus_iface_method = f'com.deepin.lastore.Updater.SetMirrorSource string:{source_id}'
    result = systemCommon.cmd_input(passwd, dbus_name, dbus_path, dbus_iface_method=dbus_iface_method)
    logging.info(result)


def setMirrorSource(passwd, source_id: str = "Aliyun", *args: str) -> bool:
    """
    SetMirrorSource:将id添加到用于下载软件的镜像源，如果添加失败，则会恢复之前的镜像源。
                    注意这里是设置中心系统更新源，不是/etc/apt/sources.list中的内容
    :param passwd:密码,修改/etc/apt/apt.conf.d/99mirrors.conf需要管理源权限
    :param source_id:调用ListMirrorSources会返回所有可用源
    :param args:其他源id
    :return: True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    mirror_sources_list_info = property_obj.ListMirrorSources(dbus.String(""))
    mirror_sources_dict_info = {str(itme[0]): str(itme[1]) for itme in mirror_sources_list_info}
    logging.info(f'mirror_sources_dict_info:\n{mirror_sources_dict_info}')

    def inner(source_id):
        logging.info(f'SetMirrorSource:设置源id为{source_id}')
        set_mirror_source(passwd, source_id)
        # property_obj.SetMirrorSource(dbus.String(source_id))
        logging.info(f'读取MirrorSource的值')
        result = getPropertiesValue(dbus.String('MirrorSource'))
        logging.info(f'MirrorSource:{result}')
        if str(result) not in mirror_sources_dict_info:
            if result == dbus.String(source_id):
                logging.info(f'目标ID不在ListMirrorSources中但可以设置成功，MirrorSource设置为 {source_id} 成功')
                raise RuntimeError('请输入正确的id值')

        if result == dbus.String(source_id):
            logging.info(f'MirrorSource设置为 {source_id} 成功')
            conf_file = '/etc/apt/apt.conf.d/99mirrors.conf'
            logging.info(f'读取{conf_file}文件中设置的MirrorSource')
            target_url = f'Acquire::SmartMirrors::MirrorSource "{mirror_sources_dict_info[str(source_id)]}";'
            with open(conf_file, 'r', encoding='utf8') as f:
                content = f.read()
                read_url = content.strip()

            if target_url == read_url:
                logging.info(f'{conf_file}设置成功')
                logging.info(f'MirrorSourceUrl：{target_url}')
                return True
            else:
                logging.info(f'{conf_file}设置失败')
                logging.info(f'target_url：{target_url}')
                logging.info(f'read_url：{read_url}')
                return False
        else:
            logging.info(f'MirrorSource设置为 {source_id} 失败')
            return False

    for _id in args:
        if not inner(_id):
            return False
    else:
        return inner(source_id)


def setErrorMirrorSource(passwd,source_id: str):
    """
    SetMirrorSource:将id添加到用于下载软件的镜像源，如果添加失败，则会恢复之前的镜像源。
                    注意这里是设置中心系统更新源，不是/etc/apt/sources.list中的内容
                    传入一个错误的id,预期设置失败
    :param passwd:密码,修改/etc/apt/apt.conf.d/99mirrors.conf需要管理源权限
    :param source_id:调用ListMirrorSources会返回所有可用源之外的id,随机输入一个字符串，如：‘xxxx’
    :return: True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    mirror_sources_list_info = property_obj.ListMirrorSources(dbus.String(""))
    mirror_sources_dict_info = {str(itme[0]): str(itme[1]) for itme in mirror_sources_list_info}
    logging.info(f'mirror_sources_dict_info:\n{mirror_sources_dict_info}')
    if str(source_id) in mirror_sources_dict_info:  # 检查传入值
        raise RuntimeError('请传入不在ListMirrorSources中的id号')

    logging.info(f'读取MirrorSource设置前的值')
    before_value = getPropertiesValue(dbus.String('MirrorSource'))
    logging.info(f'MirrorSource:{before_value}')
    logging.info(f'source_id： {source_id}')

    conf_file = '/etc/apt/apt.conf.d/99mirrors.conf'
    logging.info(f'读取设置前{conf_file}内容')

    with open(conf_file, 'r', encoding='utf8') as f:
        content = f.read()
        before_url = content.strip()

    try:
        logging.info(f'SetMirrorSource:设置源id为{source_id}')
        set_mirror_source(passwd, source_id)
        # property_obj.SetMirrorSource(dbus.String(source_id))
    except dbus.exceptions.DBusException as e:
        message = e.get_dbus_message()
        if 'not found resource: invalid mirror source id' != message:
            return False

    logging.info(f'读取MirrorSource设置后的值')
    after_value = getPropertiesValue(dbus.String('MirrorSource'))
    logging.info(f'MirrorSource:{after_value}')
    logging.info(f'source_id： {source_id}')
    if before_value != after_value:
        return False

    if after_value == dbus.String(source_id):

        logging.info(f'MirrorSource设置为 {source_id} 成功')
        return False
    else:
        logging.info(f'MirrorSource设置为 {source_id} 失败')
        logging.info(f'读取设置后{conf_file}内容')

        with open(conf_file, 'r', encoding='utf8') as f:
            content = f.read()
            after_url = content.strip()

        if before_url == after_url:
            logging.info(f'{conf_file}内容未改变')
            logging.info(f'before_url：\n{before_url}内容未改变')
            logging.info(f'target_url：\n{after_url}内容未改变')
            return True
        else:
            logging.info(f'{conf_file}内容改变')
            logging.info(f'before_url：\n{before_url}内容未改变')
            logging.info(f'target_url：\n{after_url}内容未改变')
            return False


def updatableApps():
    """
    功能：读取可更新App（应用商店软件）的信息，等同与ApplicationUpdateInfos的返回值
    方式：判读返回值类型
    :return: True or False
    """
    result = getPropertiesValue(dbus.String('UpdatableApps'))
    if isinstance(result, dbus.Array):
        logging.info(f'返回的数据类型为：{type(result)}')
        logging.info(f'result:{result}')
        return True
    else:
        logging.info(f'返回的数据类型与预期不符')
        logging.info(f'返回的数据类型为：{type(result)}')
        logging.info(f'result:{result}')
        return False


def updatablePackages():
    """
    功能：读取可更新Package的信息
    方式：判读返回值类型
    :return: True or False
    """
    result = getPropertiesValue(dbus.String('UpdatablePackages'))
    if isinstance(result, dbus.Array):
        logging.info(f'返回的数据类型为：{type(result)}')
        logging.info(f'result:{result}')
        return True
    else:
        logging.info(f'返回的数据类型与预期不符')
        logging.info(f'返回的数据类型为：{type(result)}')
        logging.info(f'result:{result}')
        return False


def autoCheckUpdates():
    """
    功能：读取是否自动更新
    方式：判读返回值类型
    :return: True or False
    """
    result = getPropertiesValue(dbus.String('AutoCheckUpdates'))
    if isinstance(result, dbus.Boolean):
        logging.info(f'返回的数据类型为：{type(result)}')
        logging.info(f'result:{result}')
        return True
    else:
        logging.info(f'返回的数据类型与预期不符')
        logging.info(f'返回的数据类型为：{type(result)}')
        logging.info(f'result:{result}')
        return False


def autoDownloadUpdates():
    """
    功能：读取是否自动下载更新包
    方式：判读返回值类型
    :return: True or False
    """
    result = getPropertiesValue(dbus.String('AutoDownloadUpdates'))
    if isinstance(result, dbus.Boolean):
        logging.info(f'返回的数据类型为：{type(result)}')
        logging.info(f'result:{result}')
        return True
    else:
        logging.info(f'返回的数据类型与预期不符')
        logging.info(f'返回的数据类型为：{type(result)}')
        logging.info(f'result:{result}')
        return False


def updateNotify():
    """
    功能：读取是否打开更新通知
    方式：判读返回值类型
    :return: True or False
    """
    result = getPropertiesValue(dbus.String('UpdateNotify'))
    if isinstance(result, dbus.Boolean):
        logging.info(f'返回的数据类型为：{type(result)}')
        logging.info(f'result:{result}')
        return True
    else:
        logging.info(f'返回的数据类型与预期不符')
        logging.info(f'返回的数据类型为：{type(result)}')
        logging.info(f'result:{result}')
        return False


def mirrorSource():
    """
    功能：读取当前镜像源
    方式：判读返回值类型，判断是否在ListMirrorSources的返回值中
    :return: True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    mirror_sources_list_info = property_obj.ListMirrorSources(dbus.String(""))
    mirror_sources_dict_info = {str(itme[0]): str(itme[1]) for itme in mirror_sources_list_info}
    logging.info(f'mirror_sources_dict_info:\n{mirror_sources_dict_info}')

    result = getPropertiesValue(dbus.String('MirrorSource'))
    if isinstance(result, dbus.String):
        logging.info(f'返回的数据类型为：{type(result)}')
        logging.info(f'result:{result}')
        if str(result) in mirror_sources_dict_info:
            logging.info('MirrorSource的值是可用源')
            return True
        else:
            logging.info('MirrorSource的值不是可用源')
            return False
    else:
        logging.info(f'返回的数据类型与预期不符')
        logging.info(f'返回的数据类型为：{type(result)}')
        logging.info(f'result:{result}')
        return False


@checkword
def getAutoInstallUpdates():
    """
    功能：是否自动安装更新
    方式：判读返回值类型
    :return: True or False
    """
    result = getPropertiesValue(dbus.String('AutoInstallUpdates'))
    if isinstance(result, dbus.Boolean):
        logging.info(f'返回的数据类型为：{type(result)}')
        logging.info(f'result:{result}')
        return True
    else:
        logging.info(f'返回的数据类型与预期不符')
        logging.info(f'返回的数据类型为：{type(result)}')
        logging.info(f'result:{result}')
        return False

@checkword
def getClassifiedUpdatablePackages():
    """
    功能：获取更新列表值
    方式：String
    :return: True or False
    """
    result = getPropertiesValue(dbus.String('ClassifiedUpdatablePackages'))
    if isinstance(result, dbus.String):
        logging.info(f'返回的数据类型为：{type(result)}')
        logging.info(f'result:{result}')
        return True
    else:
        logging.info(f'返回的数据类型与预期不符')
        logging.info(f'返回的数据类型为：{type(result)}')
        logging.info(f'result:{result}')
        return False

@checkword
def getAutoInstallUpdateType():
    """
    功能：是否自动安装更新
    方式：判读返回值类型
    :return: True or False
    """
    result = getPropertiesValue(dbus.String('AutoInstallUpdateType'))
    if isinstance(result, dbus.UInt64):
        logging.info(f'返回的数据类型为：{type(result)}')
        logging.info(f'result:{result}')
        return True
    else:
        logging.info(f'返回的数据类型与预期不符')
        logging.info(f'返回的数据类型为：{type(result)}')
        logging.info(f'result:{result}')
        return False