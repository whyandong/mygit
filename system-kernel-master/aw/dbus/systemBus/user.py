# -*- coding: utf-8 -*-
import re
import time
import pexpect
import logging

import dbus

from frame.decorator import checkword
from aw.dbus.systemBus import accounts
from subprocess import getstatusoutput

dbus_name = 'com.deepin.daemon.Accounts'
dbus_path = '/com/deepin/daemon/Accounts/User1001'
iface_name = 'com.deepin.daemon.Accounts.User'


def system_bus(user_id, bus_name='com.deepin.daemon.Accounts', iface_name='com.deepin.daemon.Accounts.User'):
    system_bus = dbus.SystemBus()
    system_obj = system_bus.get_object(bus_name, object_path='/com/deepin/daemon/Accounts/User{}'.format(user_id))
    property_obj = dbus.Interface(system_obj, dbus_interface=iface_name)
    return property_obj


def pexpect_cmd(passwd, cmd):
    ret = pexpect.spawn(cmd)
    i = ret.expect(['Passwd', pexpect.EOF, pexpect.TIMEOUT], timeout=10)
    if i == 0:
        ret.sendline(passwd)
        result = ret.read().decode(encoding="utf-8")
    else:
        b_content = ret.before
        result = str(b_content, encoding="utf-8", errors='ignore')

    return result.strip()


def cmd_input(passwd, dbus_name='com.deepin.daemon.Accounts', dbus_path=None, dbus_iface=None):
    # cmd = 'sudo dbus-send --system --print-reply  --dest={} {} {}'.format(dbus_name, dbus_path, dbus_iface)
    cmd = f'echo {passwd} | sudo -S dbus-send --system --print-reply  --dest={dbus_name} {dbus_path} {dbus_iface}'
    logging.info(cmd)
    time.sleep(1)
    getstatusoutput(cmd)
    # pexpect_cmd(passwd, cmd)


def getUserId(passwd, user_name):
    """
    动态获取用户id值
    :param passwd:用户密码
    :param user_name:用户名
    :return:用户id
    """
    time.sleep(1)
    accounts.createUser2(passwd, user_name, 1)
    user_id = accounts.findUserByName2(passwd, user_name)
    return user_id


def creatNewGroup(passwd, group_name):
    """
    新建用户组
    :param passwd:用户密码
    :param group_name:用户名
    :return:None
    """
    logging.info("新建用户组{}".format(group_name))
    cmd = f'echo {passwd} | sudo -S groupadd {group_name}'
    (status, output) = getstatusoutput(cmd)
    logging.info(f"新建用户组命令返回值{output}")


    #pexpect_cmd(passwd, 'sudo groupadd {}'.format(group_name))


def delete_group(passwd, group_name):
    """
    删除新建的用户组
    :param passwd:用户密码
    :param group_name:用户名
    :return:None
    """
    logging.info("删除用户组{}".format(group_name))
    pexpect_cmd(passwd, 'sudo groupdel {}'.format(group_name))


def addGroup(passwd, user_name, group_name):
    """
    将用户增加到用户组中
    :param passwd:用户密码
    :param group_name:用户组名
    :param user_name:用户名
    :return:None
    """
    user_id = getUserId(passwd, user_name)
    logging.info('用户{} id为{}'.format(user_name, user_id))
    creatNewGroup(passwd, group_name)
    logging.info('添加用户{}到用户组{}'.format(user_name, group_name))
    cmd_input(passwd, dbus_path='/com/deepin/daemon/Accounts/User{}'.format(user_id),
              dbus_iface="com.deepin.daemon.Accounts.User.AddGroup string:{}".format(group_name))
    time.sleep(3)


def deleteGroup(passwd, user_name, group_name):
    """
    从用户组删除用户
    :param passwd:用户密码
    :param user_name:用户名
    :param group_name:用户组名
    :return:None
    """
    ret = get_groups_detail(passwd, user_name)
    if group_name in ret:
        user_id = getUserId(passwd, user_name)
        logging.info('用户{} id为{}'.format(user_name, user_id))
        logging.info("用户组{}删除{}用户".format(group_name, user_name))
        cmd_input(passwd, dbus_path=f'/com/deepin/daemon/Accounts/User{user_id}',
                  dbus_iface=f'com.deepin.daemon.Accounts.User.DeleteGroup string:{group_name}')
    else:
        logging.info("用户组{}不存在{}用户，无需删除操作".format(group_name, user_name))


def groups(passwd, user_name):
    """
    获取用户组信息
    :param passwd: 用户密码
    :param user_name: 用户名
    :return:组信息
    """
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'Groups')
    return dbus_out


def get_groups_detail(passwd, user_name):
    """
    获取用户组详细信息
    :param passwd:用户密码
    :param user_name:用户名
    :return:list
    """
    ret = groups(passwd, user_name)
    list_ = []
    for i in range(len(ret)):
        t = re.findall(r'\S*', ret[i])
        list_.append(t[0])
    return list_


@checkword
def checkUserGroupStatus(passwd, user_name, group_name, mode):
    """
    检查用户组增加和删除用户状态
    :param passwd:用户密码
    :param user_name:用户名
    :param group_name:用户组名
    :param mode:add or del
    :return:True or False
    """
    time.sleep(2)
    list_ = get_groups_detail(passwd, user_name)
    logging.info(list_)
    if mode == 'add':
        if group_name in list_:
            logging.info("检查添加用户到用户组{}成功".format(group_name))
            return True
        else:
            logging.info("检查添加用户到用户组{}失败".format(group_name))
            return False
    elif mode == 'del':
        if group_name not in list_:
            logging.info("检查用户组{}删除用户成功".format(group_name))
            return True
        else:
            logging.info("检查用户组{}删除用户失败".format(group_name))
            return False


def setPassword(passwd, user_name):
    """
    设置用户密码
    :param passwd:用户密码
    :param user_name:用户名
    :return:None
    """
    user_id = getUserId(passwd, user_name)
    logging.info("设置账户密码")
    cmd_input(passwd, dbus_path=f'/com/deepin/daemon/Accounts/User{user_id}',
              dbus_iface='com.deepin.daemon.Accounts.User.SetPassword string:111')


def passwordStatus(passwd, user_name):
    """
    查看用户密码状态
    :param passwd:用户密码
    :param user_name:用户名
    :return:密码状态
    """
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'PasswordStatus')
    logging.info(dbus_out)
    return dbus_out


@checkword
def checkPasswordStatus(passwd, user_name):
    """
    检查设置密码成功
    :param passwd:用户密码
    :param user_name:用户名
    :return:True or False
    """
    ret = passwordStatus(passwd, user_name)
    if ret == 'P':
        logging.info("检查设置密码成功")
        return True
    else:
        logging.info("检查设置密码失败")
        return False


def enableNoPasswdLogin(passwd, user_name, mode):
    """

    :param passwd:用户密码
    :param user_name:用户名
    :param mode: enable or disable
    :return: None
    """
    time.sleep(1)
    user_id = getUserId(passwd, user_name)
    status = passwordStatus(passwd, user_name)
    if status == 'L':
        setPassword(passwd, user_name)
    if mode == 'enable':
        logging.info("设置无需密码登陆")
        cmd_input(passwd, dbus_path=f'/com/deepin/daemon/Accounts/User{user_id}',
                  dbus_iface='com.deepin.daemon.Accounts.User.EnableNoPasswdLogin boolean:true')
    elif mode == 'disable':
        logging.info("设置需密码登陆")
        cmd_input(passwd, dbus_path=f'/com/deepin/daemon/Accounts/User{user_id}',
                  dbus_iface='com.deepin.daemon.Accounts.User.EnableNoPasswdLogin boolean:false')


@checkword
def checkNoPasswdLoginStatus(passwd, user_name, mode):
    """
    检查设置无需密码登陆状态
    :param passwd: 用户密码
    :param user_name: 用户名
    :param mode:enable or disable
    :return: True or False
    """
    time.sleep(1)
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'NoPasswdLogin')
    logging.info(dbus_out)
    if mode == 'enable':
        if dbus_out:
            logging.info("检查设置无需密码登陆成功")
            return True
        else:
            logging.info("检查设置无需密码登陆失败")
            return False
    elif mode == "disable":
        if not dbus_out:
            logging.info("检查设置需密码登陆成功")
            return True
        else:
            logging.info("检查设置需密码登陆失败")
            return False


@checkword
def isPasswordExpired(passwd, user_name):
    """
    密码是否过期
    :param passwd:用户密码
    :param user_name:用户名
    :return:True or False
    """
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id)
    dbus_out = property_obj.IsPasswordExpired()
    logging.info(dbus_out)
    if not dbus_out:
        logging.info("密码没过期")
        return True
    else:
        logging.info("密码已过期")
        return False


def setAutomaticLogin(passwd, user_name, mode):
    """
    设置用户自动登陆
    :param passwd:用户密码
    :param user_name:用户名
    :param mode: True or False
    :return:None
    """
    user_id = getUserId(passwd, user_name)
    if mode:
        cmd_input(passwd, dbus_path=f'/com/deepin/daemon/Accounts/User{user_id}',
                  dbus_iface='com.deepin.daemon.Accounts.User.SetAutomaticLogin boolean:true')
    elif not mode:
        cmd_input(passwd, dbus_path=f'/com/deepin/daemon/Accounts/User{user_id}',
                  dbus_iface='com.deepin.daemon.Accounts.User.SetAutomaticLogin boolean:false')
    else:
        logging.info("参数错误，请检查")


@checkword
def automaticLogin(passwd, user_name, mode):
    """
    是否允许此用户自动登录
    :param passwd:用户密码
    :param user_name:用户名
    :param mode:True or False
    :return:True or False
    """
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'AutomaticLogin')
    logging.info(dbus_out)
    if mode:
        if dbus_out:
            logging.info("检查设置自动登录成功")
            return True
        else:
            logging.info("检查设置自动登录失败")
            return False
    else:
        if not dbus_out:
            logging.info("检查取消自动登录成功")
            return True
        else:
            logging.info("检查取消自动登录失败")
            return False


def setDesktopBackgrounds(passwd, user_name, background):
    """
    设置桌面背景
    用dbus接口弹框需要输入密码，入参为：['file:///home/test/Pictures/Wallpapers/abc-123.jpg']
    用dbus-send命令工具，入参为：array:string:'file:///usr/share/wallpapers/deepin/desktop.jpg'
    :param passwd:用户密码
    :param user_name:用户名
    :param background:桌面背景
    :return:None
    """
    user_id = getUserId(passwd, user_name)
    logging.info("获取当前桌面背景")
    getDesktopBackgrounds(passwd, user_name)
    cmd_input(passwd, dbus_path=f'/com/deepin/daemon/Accounts/User{user_id}',
              dbus_iface=f"com.deepin.daemon.Accounts.User.SetDesktopBackgrounds array:string:{background}")


def getDesktopBackgrounds(passwd, user_name):
    """
    获取当前桌面背景
    :param passwd:用户密码
    :param user_name:用户名
    :return:桌面背景信息
    """
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'DesktopBackgrounds')
    logging.info(dbus_out)
    return dbus_out


@checkword
def checkDesktopBackgrounds(passwd, user_name, background):
    """
    检查设置桌面背景成功
    :param passwd:用户密码
    :param user_name:用户名
    :param background:桌面背景信息
    :return:True or False
    """
    ret = getDesktopBackgrounds(passwd, user_name)
    if background in ret:
        logging.info("检查设置桌面背景成功")
        return True
    else:
        logging.info("检查设置桌面背景失败")
        return False


def setFullName(passwd, user_name, test_name):
    """
    修改用户名
    :param passwd:用户密码
    :param user_name:当前用户名
    :param test_name:修改后的用户名
    :return:None
    """
    user_id = getUserId(passwd, user_name)
    cmd_input(passwd, dbus_path=f'/com/deepin/daemon/Accounts/User{user_id}',
              dbus_iface=f'com.deepin.daemon.Accounts.User.SetFullName string:{test_name}')


@checkword
def fullName(passwd, user_name, test_name):
    """
    检查修改名称成功
    :param passwd:用户密码
    :param user_name:当前用户名
    :param test_name:修改后的用户名
    :return:True or False
    """
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'FullName')
    logging.info(dbus_out)
    if dbus_out == test_name:
        logging.info("检查修改名称成功")
        return True
    else:
        logging.info("检查修改名称失败")
        return False


def getGreeterBackground(passwd, user_name):
    """
    获取登录界面背景
    :param passwd:用户密码
    :param user_name:用户名
    :return:登录界面背景信息
    """
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'GreeterBackground')
    logging.info(dbus_out)
    return dbus_out


def setGreeterBackground(passwd, user_name, gre_background):
    """
    设置当前登录界面背景
    :param passwd:用户密码
    :param user_name:用户名
    :param gre_background:登录界面背景
    :return:None
    """
    user_id = getUserId(passwd, user_name)
    logging.info("获取当前登录界面背景")
    getGreeterBackground(passwd, user_name)
    cmd_input(passwd, dbus_path=f'/com/deepin/daemon/Accounts/User{user_id}',
              dbus_iface=f'com.deepin.daemon.Accounts.User.SetGreeterBackground string:{gre_background}')


@checkword
def checkGreeterBackground(passwd, user_name, gre_background):
    """
    检查设置桌面背景成功
    :param passwd:用户密码
    :param user_name:用户名
    :param gre_background:登录界面背景
    :return:True or False
    """
    ret = getGreeterBackground(passwd, user_name)
    if gre_background in ret:
        logging.info("检查设置登录背景成功")
        return True
    else:
        logging.info("检查设置登录背景失败")
        return False


def setGroups(passwd, user_name, group_name1, group_name2):
    """
    添加用户附加群组
    usermod -G user group
    :param passwd:用户密码
    :param user_name:用户名
    :param group_name1:附加组1
    :param group_name2:附加组2
    :return:None
    """
    user_id = getUserId(passwd, user_name)
    creatNewGroup(passwd, group_name1)
    creatNewGroup(passwd, group_name2)
    logging.info('添加用户{}到用户组1{}和用户组2'.format(user_name, group_name1, group_name2))
    cmd_input(passwd, dbus_path=f'/com/deepin/daemon/Accounts/User{user_id}',
              dbus_iface=f"com.deepin.daemon.Accounts.User.SetGroups array:string:{group_name1},{group_name2}")


@checkword
def checkSetGroups(passwd, user_name, group_name1, group_name2):
    """
    检查附加组增加成功
    :param passwd:用户密码
    :param user_name:用户名
    :param group_name1:附加组1
    :param group_name2:附加组2
    :return:True or False
    """
    ret = groups(passwd, user_name)
    list_ = [group_name1, group_name2]
    logging.info(ret)
    for item in list_:
        if item not in ret:
            logging.info("检查{}增加失败".format(item))
            return False
    else:
        logging.info("检查附加组增加成功")
        return True


def setLayout(passwd, user_name, layout_type):
    """
    设置键盘布局
    :param passwd:用户密码
    :param user_name:用户名
    :param layout_type: us; or cn;
    :return:None
    """
    user_id = getUserId(passwd, user_name)
    cmd_input(passwd, dbus_path=f'/com/deepin/daemon/Accounts/User{user_id}',
              dbus_iface=f"com.deepin.daemon.Accounts.User.SetLayout string:{layout_type}\\")
    time.sleep(2)


def layout(passwd, user_name):
    """
    获取当前键盘布局
    :param passwd:用户密码
    :param user_name:用户名
    :return:键盘布局信息
    """
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'Layout')
    return dbus_out


@checkword
def checkSetLayoutStatus(passwd, user_name, layout_type):
    """
    检查键盘布局设置成功
    :param passwd:用户密码
    :param user_name:用户名
    :param layout_type:us; or cn;
    :return:True or False
    """
    ret = layout(passwd, user_name)
    logging.info(f'获取到的键盘布局为{ret}')
    if layout_type in dbus.String(ret):
        logging.info("检查设置键盘布局成功")
        return True
    else:
        logging.info(f'检查设置键盘布局失败,返回值为{ret},类型为{type(ret)}')
        return False


def setLocked(passwd, user_name, mode):
    """
    锁定和解锁用户密码
    :param passwd:用户密码
    :param user_name:用户名
    :param mode: lock or unlock
    :return:None
    """
    user_id = getUserId(passwd, user_name)
    if mode == 'lock':
        cmd_input(passwd, dbus_path=f'/com/deepin/daemon/Accounts/User{user_id}',
                  dbus_iface='com.deepin.daemon.Accounts.User.SetLocked boolean:true')
    elif mode == 'unlock':
        cmd_input(passwd, dbus_path=f'/com/deepin/daemon/Accounts/User{user_id}',
                  dbus_iface='com.deepin.daemon.Accounts.User.SetLocked boolean:false')
    else:
        logging.info("参数错误，请检查")


@checkword
def locked(passwd, user_name, mode):
    """
    检查锁住和解锁用户密码成功
    :param passwd:用户密码
    :param user_name:用户名
    :param mode:lock or unlock
    :return:True or False
    """
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'Locked')
    logging.info(dbus_out)
    if mode == "lock":
        if dbus_out:
            logging.info("检查锁定用户密码成功")
            return True
        else:
            logging.info("检查锁定用户密码失败")
            return False
    if mode == "unlock":
        if not dbus_out:
            logging.info("检查解锁用户密码成功")
            return True
        else:
            logging.info("检查解锁用户密码失败")
            return False


def setIconFile(passwd, user_name, icon_file):
    """
    设置用户头像文件
    :param passwd:用户密码
    :param user_name:用户名
    :param icon_file:头像文件
    :return:
    """
    user_id = getUserId(passwd, user_name)
    logging.info("获取当前用户头像文件")
    icon_ = iconFile(passwd, user_name)
    logging.info(icon_)
    cmd_input(passwd, dbus_path=f'/com/deepin/daemon/Accounts/User{user_id}',
              dbus_iface=f'com.deepin.daemon.Accounts.User.SetIconFile string:{icon_file}')


def iconFile(passwd, user_name):
    """
    查询当前用户头像文件
    :param passwd:用户密码
    :param user_name:用户名
    :return:用户头像文件信息
    """
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'IconFile')
    return dbus_out


@checkword
def checkSetIconFileStatus(passwd, user_name, icon_file):
    """
    检查当前用户头像设置成功
    :param passwd:用户密码
    :param user_name:用户名
    :param icon_file:头像文件
    :return:True or False
    """
    ret = iconFile(passwd, user_name)
    logging.info(ret)
    if ret is not icon_file:
        logging.info("检查设置用户头像成功")
        return True
    else:
        logging.info("检查设置用户头像失败")
        return False


def setHistoryLayout(passwd, user_name, layout1, layout2):
    """
    设置历史布局
    :param passwd:用户密码
    :param user_name:用户名
    :param layout1:布局1
    :param layout2:布局2
    :return:None
    """
    user_id = getUserId(passwd, user_name)
    logging.info("获取当前历史布局")
    layout_ = historyLayout(passwd, user_name)
    logging.info(layout_)
    cmd_input(passwd, dbus_path='/com/deepin/daemon/Accounts/User{}'.format(user_id),
              dbus_iface=f'com.deepin.daemon.Accounts.User.SetHistoryLayout array:string:{layout1}\\;,{layout2}\\;')


def historyLayout(passwd, user_name):
    """
    获取当前历史布局
    :param passwd:用户密码
    :param user_name:用户名
    :return:历史布局信息
    """
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'HistoryLayout')
    return dbus_out


@checkword
def checkSetHistoryLayout(passwd, user_name, layout1, layout2):
    """
    检查设置历史布局成功
    :param passwd:用户密码
    :param user_name:用户名
    :param layout1:布局1
    :param layout2:布局2
    :return:True or False
    """
    ret = historyLayout(passwd, user_name)
    logging.info(ret)
    layout_ = [layout1, layout2]
    for item in layout_:
        if item not in dbus.String(ret):
            logging.info("检查设置历史布局{}失败".format(item))
            return False
    else:
        logging.info("检查设置历史布局成功")
        return True


def setHomeDir(passwd, user_name, home_dir):
    """
    设置家目录
    :param passwd:用户密码
    :param user_name:用户名
    :param home_dir:家目录
    :return:None
    """
    user_id = getUserId(passwd, user_name)
    logging.info("获取当前家目录")
    dir_ = homeDir(passwd, user_name)
    logging.info(dir_)
    cmd_input(passwd, dbus_path=f'/com/deepin/daemon/Accounts/User{user_id}',
              dbus_iface=f'com.deepin.daemon.Accounts.User.SetHomeDir string:{home_dir}')


def homeDir(passwd, user_name):
    """
    获取家目录
    :param passwd:用户密码
    :param user_name:用户名
    :return:家目录信息
    """
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'HomeDir')
    return dbus_out


@checkword
def checksetHomeDirStatus(passwd, user_name, home_dir):
    """
    检查设置家目录成功
    :param passwd:用户密码
    :param user_name:用户名
    :param home_dir:家目录
    :return:True or False
    """
    ret = homeDir(passwd, user_name)
    logging.info(ret)
    if ret == home_dir:
        logging.info("检查设置家目录成功")
        return True
    else:
        logging.info("检查设置家目录失败")
        return False


def setLocale(passwd, user_name, local_info):
    """
    设置本地化信息
    :param passwd:用户密码
    :param user_name:用户名
    :param local_info:本地化信息
    :return:本地化信息
    """
    user_id = getUserId(passwd, user_name)
    logging.info("获取当前本地化信息")
    local_ = locale(passwd, user_name)
    logging.info(local_)
    cmd_input(passwd, dbus_path=f'/com/deepin/daemon/Accounts/User{user_id}',
              dbus_iface=f'com.deepin.daemon.Accounts.User.SetLocale string:{local_info}')


def locale(passwd, user_name):
    """
    获取当前本地信息
    :param passwd:用户密码
    :param user_name:用户名
    :return:本地信息
    """
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'Locale')
    return dbus_out


@checkword
def checksetLocaleStatus(passwd, user_name, local_info):
    """
    检查设置本地化信息成功
    :param passwd:用户密码
    :param user_name:用户名
    :param local_info:本地化信息
    :return:True or False
    """
    ret = locale(passwd, user_name)
    logging.info(ret)
    if ret == local_info:
        logging.info("检查设置本地化信息成功")
        return True
    else:
        logging.info("检查设置本地化信息失败")
        return False


def setMaxPasswordAge(passwd, user_name, age):
    """
    设置密码有效期限
    :param passwd:用户密码
    :param user_name:用户名
    :param age:有效期限
    :return:None
    """
    user_id = getUserId(passwd, user_name)
    logging.info("获取当前密码有效期限")
    age_ = maxPasswordAge(passwd, user_name)
    logging.info(age_)
    cmd_input(passwd, dbus_path=f'/com/deepin/daemon/Accounts/User{user_id}',
              dbus_iface=f'com.deepin.daemon.Accounts.User.SetMaxPasswordAge int32:{age}')


def maxPasswordAge(passwd, user_name):
    """
    获取当前密码有效期
    :param passwd:用户密码
    :param user_name:用户名
    :return:有效期信息
    """
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'MaxPasswordAge')
    return dbus_out


@checkword
def checkSetMaxPasswordAge(passwd, user_name, age):
    """
    检查设置密码有效期限成功
    :param passwd:用户密码
    :param user_name:用户名
    :param age:有效期
    :return: True or False
    """
    ret = maxPasswordAge(passwd, user_name)
    logging.info(ret)
    if str(ret) == age:
        logging.info("检查设置密码有效期限成功")
        return True
    else:
        logging.info("检查设置密码有效期限失败")
        return False


def setShell(passwd, user_name, shell_path):
    """
    修改当前用户所用shell
    :param passwd:用户密码
    :param user_name:用户名
    :param shell_path:
    :return:None
    """
    user_id = getUserId(passwd, user_name)
    logging.info("获取当前用户所用shell")
    shell_ = getShell(passwd, user_name)
    logging.info(shell_)
    cmd_input(passwd, dbus_path=f'/com/deepin/daemon/Accounts/User{user_id}',
              dbus_iface=f'com.deepin.daemon.Accounts.User.SetShell string:{shell_path}')


def getShell(passwd, user_name):
    """
    获取当前用户所用shell
    :param passwd:用户密码
    :param user_name:用户名
    :return:shell信息
    """
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'Shell')
    return dbus_out


@checkword
def checkSetShellStatus(passwd, user_name, shell_path):
    """
    检查设置用户所用shell成功
    :param passwd:用户密码
    :param user_name:用户名
    :param shell_path:shell路径
    :return:True or False
    """
    ret = getShell(passwd, user_name)
    logging.info(ret)
    if ret == shell_path:
        logging.info("检查设置用户所用shell成功")
        return True
    else:
        logging.info("检查设置用户所用shell失败")
        return False


def setUse24HourFormat(passwd, user_name, mode):
    """
    设置时间使用24小时制
    :param passwd:用户密码
    :param user_name:用户名
    :param mode:enable or disable
    :return:
    """
    user_id = getUserId(passwd, user_name)
    logging.info("获取当前用户所用时制")
    mode_ = use24HourFormat(passwd, user_name)
    logging.info(mode_)
    if mode == 'enable':
        cmd_input(passwd, dbus_path='/com/deepin/daemon/Accounts/User{}'.format(user_id),
                  dbus_iface="com.deepin.daemon.Accounts.User.SetUse24HourFormat boolean:true")
    elif mode == 'disable':
        cmd_input(passwd, dbus_path='/com/deepin/daemon/Accounts/User{}'.format(user_id),
                  dbus_iface="com.deepin.daemon.Accounts.User.SetUse24HourFormat boolean:false")
    else:
        logging.info("传入参数不对，请检查")


def use24HourFormat(passwd, user_name):
    """
    是否使用24小时制时间
    :param passwd:用户密码
    :param user_name:用户名
    :return:时间信息
    """
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'Use24HourFormat')
    return dbus_out


@checkword
def checkSetUse24HourFormat(passwd, user_name, mode):
    """
    检查设置时间使用24小时制
    :param passwd:用户密码
    :param user_name:用户名
    :param mode:enable or disable
    :return:True or False
    """
    ret = use24HourFormat(passwd, user_name)
    logging.info(ret)
    if mode == 'enable':
        if ret == 1:
            logging.info("检查设置时间使用24小时制成功")
            return True
        else:
            logging.info("检查设置时间使用24小时制失败")
            return False
    elif mode == 'disable':
        if ret == 0:
            logging.info("检查设置时间不使用24小时制成功")
            return True
        else:
            logging.info("检查设置时间不使用24小时制失败")
            return False


@checkword
def iconList(passwd, user_name):
    """
    获取用户头像列表
    :param passwd:用户密码
    :param user_name:用户名
    :return:True or False
    """
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'IconList')
    logging.info(dbus_out)
    if dbus_out:
        logging.info("获取用户头像列表成功")
        return True
    else:
        logging.info("获取用户头像列表失败")
        return False


# @checkword
def systemAccount(passwd, user_name, mode):
    """
    检查是否是系统用户
    :param passwd:用户密码
    :param user_name:用户名
    :param mode:0：普通用户，1：系统用户
    :return:True or False
    """
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'SystemAccount')
    logging.info(dbus_out)
    logging.info(mode)
    if mode == 1:
        if dbus_out:
            logging.info("检查用户为系统用户成功")
            return True
        else:
            logging.info("检查用户为系统用户失败")
            return False
    elif mode == 0:
        if not dbus_out:
            logging.info("检查用户为普通用户成功")
            return True
        else:
            logging.info("检查用户为普通用户失败")
            return False
    else:
        logging.info("传入参数有误，请检查")
        return False


@checkword
def accountType(passwd, user_name, mode):
    """
    检查用户类型
    :param passwd:用户密码
    :param user_name:用户名
    :param mode:1 or 0
    :return:True or False
    """
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'AccountType')
    logging.info(dbus_out)
    if mode == 1:
        if dbus_out:
            logging.info("检查用户类型为系统用户成功")
            return True
        else:
            logging.info("检查用户类型为系统用户失败")
            return False
    elif mode == 0:
        if not dbus_out:
            logging.info("检查用户类型为普通用户成功")
            return True
        else:
            logging.info("检查用户类型为普通用户失败")
            return False
    else:
        logging.info("传入参数有误，请检查")
        return False


@checkword
def passwordLastChange(passwd, user_name):
    """
    最后修改密码时间
    :param passwd:用户密码
    :param user_name:用户名
    :return:True or False
    """
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'PasswordLastChange')
    logging.info(dbus_out)
    if dbus_out:
        logging.info("获取最后修改密码时间成功")
        return True
    else:
        logging.info("获取最后修改密码时间失败")
        return False


@checkword
def gid(passwd, user_name):
    """
    获取组id
    :param passwd:用户密码
    :param user_name:用户名
    :return:True or False
    """
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'Gid')
    logging.info(dbus_out)
    if dbus_out:
        logging.info("获取组id成功")
        return True
    else:
        logging.info("获取组id失败")
        return False


@checkword
def uuid(passwd, user_name):
    """
    获取dbus id
    :param passwd:用户密码
    :param user_name:用户名
    :return:True or False
    """
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'UUID')
    logging.info(dbus_out)
    if dbus_out:
        logging.info("获取dbus id成功")
        return True
    else:
        logging.info("获取dbus id失败")
        return False


@checkword
def uid(passwd, user_name):
    """
    获取用户id
    :param passwd:用户密码
    :param user_name:用户名
    :return:True or False
    """
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'Uid')
    logging.info(dbus_out)
    if dbus_out:
        logging.info("获取用户id成功")
        return True
    else:
        logging.info("获取用户id失败")
        return False


@checkword
def userName(passwd, user_name):
    """
    获取用户名
    :param passwd:用户密码
    :param user_name:用户名
    :return:True or False
    """
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'UserName')
    logging.info(dbus_out)
    if dbus_out:
        logging.info("获取用户名成功")
        return True
    else:
        logging.info("获取用户名失败")
        return False


@checkword
def xSession(passwd, user_name):
    """
    获取xSession
    :param passwd:用户密码
    :param user_name:用户名
    :return:True or False
    """
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'XSession')
    logging.info(dbus_out)
    if dbus_out:
        logging.info("获取xSession成功")
        return True
    else:
        logging.info("获取xSession失败")
        return False


@checkword
def createdTime(passwd, user_name):
    """
    获取创建用户时间
    :param passwd:用户密码
    :param user_name:用户名
    :return:True or False
    """
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'CreatedTime')
    logging.info(dbus_out)
    if dbus_out:
        logging.info("获取创建用户时间成功")
        return True
    else:
        logging.info("获取创建用户时间失败")
        return False


@checkword
def loginTime(passwd, user_name):
    """
    获取最近一次登陆时间
    :param passwd: 用户密码
    :param user_name: 用户名
    :return: True or False
    """
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'LoginTime')
    logging.info(dbus_out)
    if dbus_out == 0:
        logging.info("从未登陆过")
        return True
    else:
        logging.info("获取最近一次登陆时间失败")
        return False


def deleteIconFile(passwd, user_name):
    """
    删除不是用户当前图标的自定义图标
    :param passwd: 用户密码
    :param user_name: 用户名
    :return:
    """
    logging.info("创建非自定义图标test.png")
    cmd = 'sudo cp /var/lib/AccountsService/icons/2.png /var/lib/AccountsService/icons/test.png'
    pexpect_cmd(passwd, cmd)
    time.sleep(2)
    user_id = getUserId(passwd, user_name)
    logging.info("删除不是用户当前图标的自定义图标")
    cmd_input(passwd, dbus_path='/com/deepin/daemon/Accounts/User{}'.format(user_id),
              dbus_iface="com.deepin.daemon.Accounts.User.DeleteIconFile string:/var/lib/AccountsService/icons/test.png")


# SP3需求
def setShortDateFormat(passwd, user_name, value):
    """
    设置短日期格式
    :param passwd:用户密码
    :param user_name:用户名
    :param value:
    0表示 2020/4/5
    1表示 2020-4-5
    2表示 2020.4.5
    3表示 2020/04/05
    4表示 2020-04-05
    5表示 2020.04.05
    6表示 20/4/5
    7表示 20-4-5
    8表示 20.4.5
    :return:None
    """
    time.sleep(1)
    user_id = getUserId(passwd, user_name)
    logging.info(f"设置短日期格式{value}")
    cmd_input(passwd, dbus_path=f'/com/deepin/daemon/Accounts/User{user_id}',
              dbus_iface=f'com.deepin.daemon.Accounts.User.SetShortDateFormat int32:{value}')


def shortDateFormat(passwd, user_name):
    """
    短日期格式属性值
    :param passwd: 用户密码
    :param user_name: 用户名
    :return: dbus.Int32
    """
    time.sleep(1)
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'ShortDateFormat')
    logging.info(dbus_out)
    return dbus_out


@checkword
def checkSetShortDateFormat(passwd, user_name, value):
    """
    检查设置短日期格式状态
    :param passwd:用户密码
    :param user_name:用户名
    :param value:
    0表示 2020/4/5
    1表示 2020-4-5
    2表示 2020.4.5
    3表示 2020/04/05
    4表示 2020-04-05
    5表示 2020.04.05
    6表示 20/4/5
    7表示 20-4-5
    8表示 20.4.5
    :return:True or False
    """
    ret = shortDateFormat(passwd, user_name)
    if ret == value:
        logging.info(f"检查设置短日期格式为{value}成功")
        return True
    else:
        logging.info(f"检查设置短日期格式为{value}失败")
        return False


@checkword
def getShortDateFormat(passwd, user_name):
    """
    获取短日期格式
    :param passwd:用户密码
    :param user_name:用户名
    :return:True or False
    """
    ret = shortDateFormat(passwd, user_name)
    if isinstance(ret, dbus.Int32):
        logging.info("获取短日期格式数据成功")
        return True
    else:
        logging.info("获取短日期格式数据失败")
        return False


def setWeekdayFormat(passwd, user_name, value):
    """
    設置星期格式参数
    :param passwd: 用户密码
    :param user_name: 用户名
    :param value: 0表示 星期一, 1表示 周一
    :return:NoneType
    """
    time.sleep(1)
    user_id = getUserId(passwd, user_name)
    logging.info(f"设置星期格式{value}")
    cmd_input(passwd, dbus_path=f'/com/deepin/daemon/Accounts/User{user_id}',
              dbus_iface=f'com.deepin.daemon.Accounts.User.SetWeekdayFormat int32:{value}')



def weekdayFormat(passwd, user_name):
    """
    星期格式
    :param passwd: 用户密码
    :param user_name: 用户名
    :return: dbus.Int32
    """
    time.sleep(1)
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'WeekdayFormat')
    logging.info(dbus_out)
    return dbus_out


@checkword
def checkSetWeekdayFormat(passwd, user_name, value):
    """
    检查设置星期格式状态
    :param passwd:用户密码
    :param user_name:用户名
    :param value:0表示 星期一, 1表示 周一
    :return:True or False
    """
    ret = weekdayFormat(passwd, user_name)
    if ret == value:
        logging.info(f"检查设置星期格式为{value}成功")
        return True
    else:
        logging.info(f"检查设置星期格式为{value}失败")
        return False


@checkword
def getWeekdayFormat(passwd, user_name):
    """
    获取星期格式
    :param passwd:用户密码
    :param user_name:用户名
    :return:True or False
    """
    ret = weekdayFormat(passwd, user_name)
    if isinstance(ret, dbus.Int32):
        logging.info("获取星期格式数据成功")
        return True
    else:
        logging.info("获取星期格式数据失败")
        return False


def setLongDateFormat(passwd, user_name, value):
    """
    设置长日期格式
    :param passwd:用户密码
    :param user_name:用户名
    :param value:0表示 2020年4月5日，1表示 2020年4月5日 星期天，2表示 星期天 2020年4月5日
    :return:None
    """
    time.sleep(1)
    user_id = getUserId(passwd, user_name)
    logging.info(f"设置长日期格式{value}")
    cmd_input(passwd, dbus_path=f'/com/deepin/daemon/Accounts/User{user_id}',
              dbus_iface=f'com.deepin.daemon.Accounts.User.SetLongDateFormat int32:{value}')


def longDateFormat(passwd, user_name):
    """
    长日期格式属性值
    :param passwd: 用户密码
    :param user_name: 用户名
    :return: dbus.Int32
    """
    time.sleep(1)
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'LongDateFormat')
    logging.info(dbus_out)
    return dbus_out


@checkword
def checkSetLongDateFormat(passwd, user_name, value):
    """
    检查设置长日期格式状态
    :param passwd:用户密码
    :param user_name:用户名
    :param value:0表示 2020年4月5日，1表示 2020年4月5日 星期天，2表示 星期天 2020年4月5日
    :return:True or False
    """
    ret = longDateFormat(passwd, user_name)
    if ret == value:
        logging.info(f"检查设置长日期格式为{value}成功")
        return True
    else:
        logging.info(f"检查设置长日期格式为{value}失败")
        return False


@checkword
def getLongDateFormat(passwd, user_name):
    """
    获取长日期格式
    :param passwd:用户密码
    :param user_name:用户名
    :return:True or False
    """
    ret = longDateFormat(passwd, user_name)
    if isinstance(ret, dbus.Int32):
        logging.info("获取长日期格式数据成功")
        return True
    else:
        logging.info("获取长日期格式数据失败")
        return False


def setShortTimeFormat(passwd, user_name, value):
    """
    设置短时间格式
    :param passwd:用户密码
    :param user_name:用户名
    :param value:0表示 9：7，1 表示 09：07，2表示 9：7 AM，3表示 09：07 AM
    :return:None
    """
    time.sleep(1)
    user_id = getUserId(passwd, user_name)
    logging.info(f"设置短时间格式{value}")
    cmd_input(passwd, dbus_path=f'/com/deepin/daemon/Accounts/User{user_id}',
              dbus_iface=f'com.deepin.daemon.Accounts.User.SetShortTimeFormat int32:{value}')


def shortTimeFormat(passwd, user_name):
    """
    短时间格式属性值
    :param passwd: 用户密码
    :param user_name: 用户名
    :return: dbus.Int32
    """
    time.sleep(1)
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'ShortTimeFormat')
    logging.info(dbus_out)
    return dbus_out


@checkword
def checkSetShortTimeFormat(passwd, user_name, value):
    """
    检查设置短时间格式状态
    :param passwd:用户密码
    :param user_name:用户名
    :param value:0表示 9：7，1 表示 09：07，2表示 9：7 AM，3表示 09：07 AM
    :return:True or False
    """
    ret = shortTimeFormat(passwd, user_name)
    if ret == value:
        logging.info(f"检查设置短时间格式为{value}成功")
        return True
    else:
        logging.info(f"检查设置短时间格式为{value}失败")
        return False


@checkword
def getShortTimeFormat(passwd, user_name):
    """
    获取短时间格式
    :param passwd:用户密码
    :param user_name:用户名
    :return:True or False
    """
    ret = shortTimeFormat(passwd, user_name)
    if isinstance(ret, dbus.Int32):
        logging.info("获取短时间格式数据成功")
        return True
    else:
        logging.info("获取短时间格式数据失败")
        return False


def setLongTimeFormat(passwd, user_name, value):
    """
    设置长时间格式
    :param passwd:用户密码
    :param user_name:用户名
    :param value:0表示 9：7：20 ，1 表示 09：07：20，2表示 9：7：20 AM，3表示 09：07：20 AM
    :return:None
    """
    time.sleep(1)
    user_id = getUserId(passwd, user_name)
    logging.info(f"设置长时间格式{value}")
    cmd_input(passwd, dbus_path=f'/com/deepin/daemon/Accounts/User{user_id}',
              dbus_iface=f'com.deepin.daemon.Accounts.User.SetLongTimeFormat int32:{value}')


def longTimeFormat(passwd, user_name):
    """
    长时间格式属性值
    :param passwd: 用户密码
    :param user_name: 用户名
    :return: dbus.Int32
    """
    time.sleep(1)
    user_id = getUserId(passwd, user_name)
    property_obj = system_bus(user_id, iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts.User', 'LongTimeFormat')
    logging.info(dbus_out)
    return dbus_out


@checkword
def checkSetLongTimeFormat(passwd, user_name, value):
    """
    检查设置长时间格式状态
    :param passwd:用户密码
    :param user_name:用户名
    :param value:0表示 9：7：20 ，1 表示 09：07：20，2表示 9：7：20 AM，3表示 09：07：20 AM
    :return:True or False
    """
    ret = longTimeFormat(passwd, user_name)
    if ret == value:
        logging.info(f"检查设置长时间格式为{value}成功")
        return True
    else:
        logging.info(f"检查设置长时间格式为{value}失败")
        return False


@checkword
def getLongTimeFormat(passwd, user_name):
    """
    获取长时间格式
    :param passwd:用户密码
    :param user_name:用户名
    :return:True or False
    """
    ret = longTimeFormat(passwd, user_name)
    if isinstance(ret, dbus.Int32):
        logging.info("获取长时间格式数据成功")
        return True
    else:
        logging.info("获取长时间格式数据失败")
        return False

