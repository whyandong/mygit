# -*- coding: utf-8 -*-
import logging
import time
import dbus

from aw.dbus.systemBus import systemCommon
from frame.decorator import checkword
from subprocess import getstatusoutput

dbus_name = 'com.deepin.lastore'
dbus_path = '/com/deepin/lastore'
iface_name = 'com.deepin.lastore.Manager'


def cmd_input(passwd, dbus_name=dbus_name, dbus_path=dbus_path, dbus_iface=iface_name):
    cmd = f'echo {passwd} | sudo -S dbus-send --system --print-reply  --dest={dbus_name} {dbus_path} {dbus_iface}'
    time.sleep(1)
    logging.info(cmd)
    (status, output) = getstatusoutput(cmd)
    logging.info(output)
    if status == 0:
        logging.info(f'命令执行成功{status}')
        return status, output
    else:
        logging.info(f'命令执行失败{status}')
        return status, output


@checkword
def classifiedUpgrade(updatetype):
    """
    根据传入的类别,完成下载和安装更新
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    out = property_obj.ClassifiedUpgrade(updatetype)
    logging.info(out)
    if isinstance(out, dbus.String):
        logging.info("根据传入的类别,返回下载和安装更新成功")
        return True
    else:
        logging.info("根据传入的类别,返回下载和安装更新失败")
        return False


@checkword
def cleanArchives():
    """
    创建一个清理任务
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    out = property_obj.CleanArchives()
    logging.info(out)
    if out:
        logging.info("创建一个清理任务成功")
        return True
    else:
        logging.info("创建一个清理任务失败")
        return False


def setAutoClean(mode):
    """
    设置是否自动清理
    :param mode:enable or disable
    :return:None
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    if mode == 'enable':
        out = property_obj.SetAutoClean(True)
        logging.info(out)
    elif mode == 'disable':
        out = property_obj.SetAutoClean(False)
        logging.info(out)
    else:
        logging.info("参数传入错误，请检查！")


def autoClean():
    """
    是否自动清理
    :return:bool
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    out = property_obj.Get('com.deepin.lastore.Manager', 'AutoClean')
    logging.info(out)
    return out


def getAutoCleanStatus():
    """
    获取自动清理状态
    :return:True or False
    """
    ret = autoClean()
    if ret == 1 or ret == 0:
        logging.info("检查获取自动清理状态{}成功".format(ret))
        return True
    else:
        logging.info("检查获取自动清理状态失败")
        return False


@checkword
def checkAutoCleanStatus(mode):
    """
    检查自动清理状态
    :param mode:enable or disable
    :return:True or False
    """
    ret = autoClean()
    if mode == 'enable':
        if ret == 1:
            logging.info('检查打开自动清理成功')
            return True
        else:
            logging.info('检查打开自动清理失败')
            return False
    elif mode == 'disable':
        if not ret:
            logging.info('检查关闭自动清理成功')
            return True
        else:
            logging.info('检查关闭自动清理失败')
            return False
    else:
        logging.info('参数错误，请检查！')
        return False


def updateSource():
    """
    创建一个更新源的任务
    :return:None
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    property_obj.UpdateSource()


@checkword
def cleanJob(jobid):
    """
    清理一个任务，若任务正在运行，则暂停它
    :param jobid:任务id
    :return:True or False
    """
    updateSource()
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    out = property_obj.CleanJob(jobid)
    logging.info(out)
    if not out:
        logging.info("清理任务成功")
        return True
    else:
        logging.info("清理任务失败")
        return False


@checkword
def fixError(errType):
    """
    创建一个修复错误的任务，检查更新源
    :param errType:错误类型
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    out = property_obj.FixError(errType)
    logging.info(out)
    if out:
        logging.info('创建修复{}错误的任务成功'.format(errType))
        return True
    else:
        logging.info('创建修复{}错误的任务失败'.format(errType))
        return False


@checkword
def packageExists(mode, pkgId):
    """
    查询软件是否安装
    :param mode:install or uninstall
    :param pkgId:软件名
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    out = property_obj.PackageExists(pkgId)
    logging.info(out)
    if mode == 'install':
        if out:
            logging.info('查询软件已安装成功')
            return True
        else:
            logging.info('查询软件已安装失败')
            return False
    elif mode == 'uninstall':
        if not out:
            logging.info('查询软件未安装成功')
            return True
        else:
            logging.info('查询软件未安装失败')
            return False
    else:
        logging.info("参数传入错误，请检查！")
        return False


@checkword
def packageDesktopPath(mode, pkgId):
    """
    获取软件的执行路径
    :param mode: install or uninstall
    :param pkgId: 安装包id，如deepin-music
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    out = property_obj.PackageDesktopPath(pkgId)
    logging.info(out)
    if mode == 'install':
        if out:
            logging.info('查询已安装软件的执行路径成功')
            return True
        else:
            logging.info('查询已安装软件的执行路径失败')
            return False
    elif mode == 'uninstall':
        if not out:
            logging.info('查询未安装软件路径为空成功')
            return True
        else:
            logging.info('查询未安装软件路径为空失败')
            return False
    else:
        logging.info("参数传入错误，请检查！")
        return False


@checkword
def packageInstallable(mode, pkgId):
    """
    查询软件是否可以安装
    :param mode: valid or invalid
    :param pkgId: 安装包id，如deepin-music
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    out = property_obj.PackageInstallable(pkgId)
    logging.info(out)
    if mode == 'valid':
        if out:
            logging.info('查询有效软件可以安装成功')
            return True
        else:
            logging.info('查询有效软件可以安装失败')
            return False
    elif mode == 'invalid':
        if not out:
            logging.info('查询无效软件不可以安装成功')
            return True
        else:
            logging.info('查询无效软件不可以安装失败')
            return False
    else:
        logging.info("参数传入错误，请检查！")
        return False


@checkword
def packagesDownloadSize(pkgs):
    """
    获取软件包的下载大小
    :param pkgs: 软件包列表，如['deepin-appstore','deepin-contacts']
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    out = property_obj.PackagesDownloadSize(pkgs)
    logging.info(out)
    type = isinstance(out, int)
    logging.info(type)
    if type:
        logging.info('获取软件包的下载大小成功')
        return True
    else:
        logging.info('获取软件包的下载大小失败')
        return False


@checkword
def updateSource():
    """
    创建一个更新源的任务，并返回任务的路径
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    out = property_obj.UpdateSource()
    logging.info(out)
    str_ = '/com/deepin/lastore/Jobupdate_source'
    if out in str_:
        logging.info('创建一个更新源的任务成功')
        return True
    else:
        logging.info('创建一个更新源的任务失败')
        return False


def prepareDistUpgrade():
    """
    开启一个预更新的任务，并返回此任务的路径
    :return:Object Path job
    """
    try:
        property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
        dbus_out = property_obj.PrepareDistUpgrade()
        return dbus_out
    except dbus.exceptions.DBusException as e:
        return str(e)


@checkword
def checkPrepareDistUpgradeStatus():
    """
    检查预更新操作状态
    :return: True or False
    """
    ret = prepareDistUpgrade()
    logging.info(ret)
    str_ = '/com/deepin/lastore/Jobprepare_dist_upgrade'
    if 'no need download' or 'empty UpgradableApps' in ret:
        logging.info('系统无需下载任务，检查无需开启预更新成功')
        return True
    elif str_ in ret:
        logging.info('检查开启一个预更新的任务成功')
        return True
    else:
        logging.info('检查开启一个预更新的任务失败')
        return False


def distUpgrade():
    """
    创建一个升级任务
    :return:Object Path job
    """
    try:
        property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
        dbus_out = property_obj.DistUpgrade()
        return dbus_out
    except dbus.exceptions.DBusException as e:
        print(e)
        return str(e)


@checkword
def checkDistUpgradeStatus():
    """
    检查升级状态
    :return: True or False
    """
    ret = distUpgrade()
    logging.info(ret)
    str_ = '/com/deepin/lastore/Joblist_upgrade'
    if 'empty UpgradableApps' in ret:
        logging.info('系统已最新，检查无需升级成功')
        return True
    elif str_ in ret:
        logging.info('检查升级成功')
        return True
    else:
        logging.info('检查升级失败')
        return False


@checkword
def updatePackage(jobName, pkg):
    """
    升级软件包
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    out = property_obj.UpdatePackage(jobName, pkg)
    logging.info(out)
    str_ = '/com/deepin/lastore/'
    if str_ in out:
        logging.info('升级软件包成功')
        return True
    else:
        logging.info('升级软件包失败')
        return False


@checkword
def jobList():
    """
    获取任务列表
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    out = property_obj.Get('com.deepin.lastore.Manager', 'JobList')
    logging.info(out)
    if isinstance(out, dbus.Array):
        logging.info("获取任务操作成功")
        return True
    else:
        logging.info("获取任务操作失败")
        return False


@checkword
def systemArchitectures():
    """
    获取系统架构信息
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    out = property_obj.Get('com.deepin.lastore.Manager', 'SystemArchitectures')
    logging.info(out)
    if out:
        logging.info("获取系统架构信息成功")
        return True
    else:
        logging.info("获取系统架构信息失败")
        return False


@checkword
def upgradableApps():
    """
    获取可以升级的软件
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    out = property_obj.Get('com.deepin.lastore.Manager', 'UpgradableApps')
    logging.info(out)
    if isinstance(out, dbus.Array):
        logging.info("获取可以升级的软件信息成功")
        return True
    else:
        logging.info("获取可以升级的软件信息失败")
        return False


@checkword
def systemOnChanging():
    """
    是否正在更新中
    :return: True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    out = property_obj.Get('com.deepin.lastore.Manager', 'SystemOnChanging')
    logging.info(out)
    if isinstance(out, dbus.Boolean):
        logging.info("获取系统更新状态成功")
        return True
    else:
        logging.info("获取系统更新状态失败")
        return False


@checkword
def handleSystemEvent(passwd, eventType):
    """
    监控处理系统事件类型，检验执行状态
    :params: passwd：管理用户密码执行；eventType：系统事件类型
    :return: 无
    """
    status, out = cmd_input(passwd,
                            dbus_iface='com.deepin.lastore.Manager.HandleSystemEvent string:"{}"'.format(eventType))
    if status == 0:
        logging.info(f"处理系统事件{eventType}成功,返回状态:{status}")
        return True
    else:
        logging.info(f"处理系统事件{eventType}失败,返回状态:{status}")
        return False
