# -*- coding: utf-8 -*-
import os
import re
import dbus
import time
import pexpect
import logging
import threading
import subprocess

from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop

DBusGMainLoop(set_as_default=True)

from frame import constant
from frame.decorator import checkword
from subprocess import getstatusoutput


def system_bus(dbus_name='com.deepin.daemon.Grub2', dbus_path='/com/deepin/daemon/Grub2',
               iface_name='com.deepin.daemon.Grub2'):
    system_bus = dbus.SystemBus()
    system_obj = system_bus.get_object(dbus_name, dbus_path)
    property_obj = dbus.Interface(system_obj, dbus_interface=iface_name)
    return property_obj


def cmd_input(passwd, dbus_name='com.deepin.daemon.Grub2', dbus_path='/com/deepin/daemon/Grub2', dbus_iface=None):
    #cmd = 'sudo dbus-send --system --print-reply  --dest={} {} {}'.format(dbus_name, dbus_path, dbus_iface)
    cmd = f'echo {passwd} | sudo -S dbus-send --system --print-reply  --dest={dbus_name} {dbus_path} {dbus_iface}'
    time.sleep(1)
    logging.info(cmd)
    #ret = pexpect.spawn(cmd)
    # i = ret.expect('sudo', timeout=5)
    # if i == 0:
    #     ret.sendline(passwd)
    # return ret.readlines()
    (status, output) = getstatusoutput(cmd)
    if status == 0:
        logging.info("命令执行成功")
    else:
        logging.info("命令执行失败")


    # i = ret.expect(['密码', pexpect.EOF, pexpect.TIMEOUT], timeout=10)
    # if i == 0:
    #     ret.sendline(passwd)
    #     result = ret.read().decode(encoding="utf-8")
    # else:
    #     b_content = ret.before
    #     result = str(b_content, encoding="utf-8", errors='ignore')
    #
    # return result.strip()

@checkword
def getAvailableGfxmodes():
    """
    用于获取所有GRUB引导菜单可显示的图像输出分辨率
    :param mode:enable or disable
    :return: True or False
    """
    time.sleep(1)
    property_obj = system_bus()
    dbus_out = property_obj.GetAvailableGfxmodes()
    logging.info(dbus_out)
    if isinstance(dbus_out, dbus.Array):
        logging.info("获取GRUB引导菜单可显示的图像输出分辨率成功")
        return True
    else:
        logging.info("获取GRUB引导菜单可显示的图像输出分辨率失败")
        return False


@checkword
def gfxmode():
    """
    当前GRUB引导菜单显示的分辨率
    :return: True or False
    """
    time.sleep(1)
    property_obj = system_bus(iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Grub2', 'Gfxmode')
    logging.info(dbus_out)
    if dbus_out:
        logging.info("GRUB引导菜单显示的分辨率正常")
        return True
    else:
        logging.info("GRUB引导菜单显示的分辨率异常")
        return False


@checkword
def getSimpleEntryTitles():
    """
    用于获取GRUB引导菜单显示的标题
    :return:True or False
    """
    time.sleep(2)
    property_obj = system_bus()
    dbus_out = property_obj.GetSimpleEntryTitles()
    logging.info(dbus_out)
    list_ = [str(x) for x in dbus_out]
    logging.info(list_)
    ret = defaultEntry()
    if ret in list_:
        logging.info("获取GRUB引导菜单显示的标题成功")
        return True
    else:
        logging.info("获取GRUB引导菜单显示的标题失败")
        return False


def defaultEntry():
    """
    GRUB引导菜单默认的启动项
    :return:string
    """
    property_obj = system_bus(iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Grub2', 'DefaultEntry')
    logging.info(dbus_out)
    return dbus_out


@checkword
def getDefaultEntry():
    """
    获取GRUB引导菜单默认的启动项
    :return: True or False
    """
    ret = defaultEntry()
    if ret:
        logging.info("获取GRUB引导菜单默认的启动项成功")
        return True
    else:
        logging.info("获取GRUB引导菜单默认的启动项失败")
        return False


def reset(passwd):
    """
    重置所有的设置
    :param passwd:用户密码
    :return:None
    """
    cmd_input(passwd, dbus_iface='com.deepin.daemon.Grub2.Reset')
    time.sleep(2)


def setEnableTheme(passwd, mode):
    """
    用于设置GRUB菜单中是否开启主题
    :param passwd: 用户密码
    :param mode: enable or disable
    :return: None
    """
    time.sleep(2)
    if mode == 'enable':
        logging.info("设置Grub开启主题")
        out = cmd_input(passwd, dbus_iface='com.deepin.daemon.Grub2.SetEnableTheme boolean:true')
        logging.info(out)
    elif mode == 'disable':
        logging.info("设置Grub关闭主题")
        out = cmd_input(passwd, dbus_iface='com.deepin.daemon.Grub2.SetEnableTheme boolean:false')
        logging.info(out)
    else:
        logging.info("传入参数有误，请检查")


def enableTheme():
    """
    是否开启了GRUB菜单主题
    :return: string
    """
    property_obj = system_bus(iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Grub2', 'EnableTheme')
    logging.info(dbus_out)
    return dbus_out


def checkThemeStatus(mode):
    """
    检查开启主题状态
    :param mode:enable or disable
    :return:True or False
    """
    ret = enableTheme()
    if mode == 'enable':
        if ret:
            logging.info("检查开启主题成功")
            return True
        else:
            logging.info("检查开启主题失败")
            return False
    elif mode == 'disable':
        if not ret:
            logging.info("检查关闭主题成功")
            return True
        else:
            logging.info("检查关闭主题失败")
            return False


def setTimeout(passwd, time_out):
    """
    用于设置用户无操作时,在GRUB菜单界面的停留时间
    :param passwd: 用户密码
    :param time_out: 界面的停留时间
    :return:None
    """
    cmd_input(passwd, dbus_iface='com.deepin.daemon.Grub2.SetTimeout uint32:{}'.format(time_out))


def getTimeout():
    """
    获取当前超时时间
    :return: string
    """
    property_obj = system_bus(iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Grub2', 'Timeout')
    logging.info(dbus_out)
    return dbus_out


@checkword
def checkSetTimeout(time_out):
    """
    检查超时时间设置成功
    :param time_out:超时时间
    :return: True or False
    """
    ret = getTimeout()
    logging.info(ret)
    if str(ret) == time_out:
        logging.info("设置超时时间成功")
        return True
    else:
        logging.info("设置超时时间失败")
        return False


def getSystemDefaultEntry():
    """
    仅功能函数，不断言，获取当前系统启动项列表
    :return: list
    """
    property_obj = system_bus()
    dbus_out = property_obj.GetSimpleEntryTitles()
    list_ = [str(x) for x in dbus_out]
    first_entry = list_[0]
    end_entry = list_[-1]
    return first_entry, end_entry


def setDefaultEntry(passwd, entry_type):
    """
    用于设置GRUB引导菜单的默认入口
    :param passwd:用户密码
    :param entry_type: 入口类型
    :return:None
    """
    first_entry, end_entry = getSystemDefaultEntry()
    if entry_type == 'first_entry':
        cmd_input(passwd, dbus_iface='com.deepin.daemon.Grub2.SetDefaultEntry string:"{}"'.format(first_entry))
        logging.info('设置默认入口为{}'.format(first_entry))
    elif entry_type == 'end_entry':
        cmd_input(passwd, dbus_iface='com.deepin.daemon.Grub2.SetDefaultEntry string:"{}"'.format(end_entry))
        logging.info('设置默认入口为{}'.format(end_entry))
    else:
        logging.info("传入参数有误，请检查")


@checkword
def checkSetDefaultEntry(entry_type):
    """
    检查设置默认入口状态
    :param entry_type: 入口类型
    :return:True or False
    """
    ret = defaultEntry()
    first_entry, end_entry = getSystemDefaultEntry()
    if entry_type == 'first_entry':
        if ret == first_entry:
            logging.info("检查设置GRUB引导菜单的默认入口为{}成功".format(first_entry))
            return True
        else:
            logging.info("检查设置GRUB引导菜单的默认入口为{}失败".format(first_entry))
            return False
    elif entry_type == 'end_entry':
        if ret == end_entry:
            logging.info("检查设置GRUB引导菜单的默认入口为{}成功".format(end_entry))
            return True
        else:
            logging.info("检查设置GRUB引导菜单的默认入口为{}失败".format(end_entry))
            return False


@checkword
def getEnableTheme():
    """
    获取是否开启了GRUB菜单主题状态值
    :return:True or False
    """
    ret = enableTheme()
    if ret == 1 or ret == 0:
        logging.info("获取是否开启了GRUB菜单主题成功")
        return True
    else:
        logging.info("获取是否开启了GRUB菜单主题失败")
        return False


@checkword
def getUpdating():
    """
    当前是否处于系统更新状态
    :return:True or False
    """
    property_obj = system_bus(iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Grub2', 'Updating')
    logging.info(dbus_out)
    if dbus_out == 0 or dbus_out:
        logging.info("获取当前是否处于系统更新状态成功")
        return True
    else:
        logging.info("获取当前是否处于系统更新状态失败")
        return False


@checkword
def getThemeFile():
    """
    在开启了GRUB菜单主题后,使用的主题文件
    :return:True or False
    """
    property_obj = system_bus(iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Grub2', 'ThemeFile')
    logging.info(dbus_out)
    if dbus_out:
        logging.info("获取使用的主题文件成功")
        return True
    else:
        logging.info("获取使用的主题文件失败")
        return False


@checkword
def timeOut():
    """
    获取用户无操作时,在GRUB菜单界面的停留时间
    :return:True or False
    """
    property_obj = system_bus(iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Grub2', 'Timeout')
    logging.info(dbus_out)
    if dbus_out:
        logging.info("获取用户无操作时,停留时间成功")
        return True
    else:
        logging.info("获取用户无操作时,停留时间失败")
        return False


# grubTheme模块

@checkword
def getBackground():
    """
    用于获取GRUB引导菜单的背景文件的绝对路径
    :return: True or False
    """
    property_obj = system_bus(dbus_name='com.deepin.daemon.Grub2', dbus_path='/com/deepin/daemon/Grub2/Theme',
                              iface_name='com.deepin.daemon.Grub2.Theme')
    dbus_out = property_obj.GetBackground()
    logging.info(dbus_out)
    if isinstance(dbus_out, dbus.String):
        logging.info("获取GRUB引导菜单的背景文件的绝对路径成功")
        return True
    else:
        logging.info("获取GRUB引导菜单的背景文件的绝对路径失败")
        return False


def setBackgroundSourceFile(passwd, filename):
    """
    设置GRUB引导菜单的背景文件的绝对路径
    :param passwd: 用户密码
    :param filename:文件名
    :return:
    """
    cmd_input(passwd, dbus_path='/com/deepin/daemon/Grub2/Theme',
              dbus_iface='com.deepin.daemon.Grub2.Theme.SetBackgroundSourceFile string:{}'.format(filename))


def excute_cmd(cmd):
    """
    执行cmd命令
    :param cmd:输入命令
    :return:string
    """
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, encoding='utf-8')

    outMsg = p.stdout.read()
    errMsg = p.stderr.read()
    if errMsg:
        return errMsg
    else:
        return outMsg


def getBackgroundSourceFileSize():
    """
    获取/boot/grub/themes/deepin/文件大小
    :return:int
    """
    out = excute_cmd('ls -lh /boot/grub/themes/deepin/')
    file_size = out.split('\n')[0].split(' ')[-1:][0]
    logging.info(file_size)
    return file_size


@checkword
def checkSetBackgroundSourceFile():
    """
    检查设置GRUB引导菜单的背景文件的绝对路径成功
    :return:True or False
    """
    ret0 = getBackgroundSourceFileSize()
    if ret0 not in '11M':
        logging.info("检查设置GRUB引导菜单的背景文件的绝对路径成功")
        return True
    else:
        logging.info("检查设置GRUB引导菜单的背景文件的绝对路径失败")
        return False


def send_signal(passwd, filename):
    """
    设置GRUB引导菜单的背景文件的绝对路径（触发信号）
    :param passwd: 用户密码
    :param filename:文件名
    :return:None
    """
    logging.info("开始发送触发信号")
    logging.info("开始设置GRUB引导菜单的背景文件的绝对路径")
    setBackgroundSourceFile(passwd, filename)


def signal_handler(*args, **kwargs):
    dbus_path0 = constant.dbus_path
    kwarg = str(kwargs)
    cmd = 'echo ' + kwarg + '>> {}/sourceFile_signal.log'.format(dbus_path0)
    logging.info(cmd)
    os.system(cmd)


def receive_signal():
    """
    接收信号
    :return:None
    """
    logging.info("启动监护线程，接收signal信号")
    bus = dbus.SystemBus()
    bus.add_signal_receiver(signal_handler, bus_name='com.deepin.daemon.Grub2', member_keyword='member')
    loop = GLib.MainLoop()
    loop.run()


@checkword
def check_signal():
    """
    检查信号接收状态
    :return:True or False
    """
    logging.info("开始检查接收信号内容是否正确")
    dbus_path0 = constant.dbus_path
    my_file = '{}/sourceFile_signal.log'.format(dbus_path0)
    loop = 10
    while loop:
        time.sleep(2)
        if os.path.exists(my_file):
            logging.info("收集信号完成")
            with open(my_file) as f:
                content = f.readlines()
            list_ = []
            for i in content:
                pattern = r'BackgroundChanged'
                t = re.findall(pattern, i)
                if t:
                    list_.append(t[0])
            logging.info("收集到的信号内容为：{}".format(list_))
            if 'BackgroundChanged' in list_:
                logging.info("检查接收BackgroundChanged信号成功")
                return True
            else:
                logging.info("检查接收BackgroundChanged信号失败")
                return False
        else:
            logging.info("收集信号还没完成,继续等待")
            loop = loop - 1
    else:
        logging.info("等待超时，请重新收集")
        return False


def backGroundChanged(passwd, filename):
    """
    监控GRUB引导菜单背景修改时信号
    :param passwd:用户密码
    :param filename:文件名
    :return:None
    """
    dbus_path0 = constant.dbus_path
    my_file = '{}/sourceFile_signal.log'.format(dbus_path0)
    if os.path.exists(my_file):
        os.remove(my_file)
        logging.info("删除已存在sourceFile_signal.log文件")

    threads = []
    my_thread1 = threading.Thread(target=receive_signal)
    threads.append(my_thread1)

    my_thread2 = threading.Thread(target=send_signal, args=(passwd, filename))
    threads.append(my_thread2)

    my_thread1.setDaemon(True)

    for i in threads:
        i.start()
    time.sleep(5)
    check_signal()
    if os.path.exists(my_file):
        os.remove(my_file)
        logging.info("删除已存在sourceFile_signal.log文件")
    logging.info("主线程结束")
