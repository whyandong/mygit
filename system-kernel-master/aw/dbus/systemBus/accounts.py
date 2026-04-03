# -*- coding: utf-8 -*-
import os
import re
import dbus
import time
import pexpect
import logging
import threading

from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop
from subprocess import getstatusoutput

DBusGMainLoop(set_as_default=True)

from frame import constant
from frame.decorator import checkword


def system_bus(dbus_name='com.deepin.daemon.Accounts', dbus_path='/com/deepin/daemon/Accounts',
               iface_name='com.deepin.daemon.Accounts'):
    system_bus = dbus.SystemBus()
    system_obj = system_bus.get_object(dbus_name, dbus_path)
    property_obj = dbus.Interface(system_obj, dbus_interface=iface_name)
    return property_obj


def cmd_input(passwd, dbus_name='com.deepin.daemon.Accounts', dbus_path='/com/deepin/daemon/Accounts',
              dbus_iface='com.deepin.daemon.Accounts.AllowGuestAccount boolean:true'):
    # cmd = 'sudo dbus-send --system --print-reply  --dest={} {} {}'.format(dbus_name, dbus_path, dbus_iface)
    cmd = f'echo {passwd} | sudo -S dbus-send --system --print-reply  --dest={dbus_name} {dbus_path} {dbus_iface}'
    time.sleep(1)
    logging.info(cmd)
    (status, output) = getstatusoutput(cmd)
    if status == 0:
        logging.info("命令执行成功")
    else:
        logging.info("命令执行失败")

    # if i == 0:
    #     ret.sendline(passwd)
    #     result = ret.read().decode(encoding="utf-8")
    # else:
    #     b_content = ret.before
    #     result = str(b_content, encoding="utf-8", errors='ignore')
    #
    # return result.strip()


def allowGuestAccount(passwd, mode):
    """
    设置允许来宾用户
    :param passwd:用户密码
    :param mode:enable or disable
    :return:None
    """
    time.sleep(2)
    if mode == 'enable':
        logging.info("设置允许来宾账户")
        cmd_input(passwd, dbus_iface='com.deepin.daemon.Accounts.AllowGuestAccount boolean:true')
    elif mode == 'disable':
        logging.info("设置不允许来宾账户")
        cmd_input(passwd, dbus_iface='com.deepin.daemon.Accounts.AllowGuestAccount boolean:false')


@checkword
def getAllowGuestStatus(mode):
    """
    检查设置允许来宾用户状态
    :param mode:enable or disable
    :return:True or False
    """
    time.sleep(2)
    property_obj = system_bus(iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts', 'AllowGuest')
    logging.info(dbus_out)
    if mode == 'enable':
        if dbus_out:
            logging.info("检查设置允许来宾账户成功")
            return True
        else:
            logging.info("检查设置允许来宾账户失败")
            return False
    elif mode == "disable":
        if not dbus_out:
            logging.info("检查设置不允许来宾账户成功")
            return True
        else:
            logging.info("检查设置不允许来宾账户失败")
            return False


@checkword
def createGuestAccount(passwd):
    """
    创建一个来宾账户,并检查创建成功
    :param passwd: 用户密码
    :return: True or False
    """
    cmd_input(passwd, dbus_iface='com.deepin.daemon.Accounts.CreateGuestAccount')
    return True
    # t = re.findall(r'"(\S*)"', out)
    # logging.info("新建来宾账户路径为：{}".format(t[0]))
    # time.sleep(2)
    # res = getUserList()
    # for i in range(len(res)):
    #     if t[0] == res[i]:
    #         logging.info("检查新建{}成功".format(res[i]))
    #         return True
    #     else:
    #         time.sleep(0.5)
    #         continue
    # else:
    #     logging.info("检测创建的来宾账户失败")
    #     return False


def getUserList():
    """
    获取用户列表
    :return: list
    """
    time.sleep(2)
    property_obj = system_bus(iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts', 'UserList')
    list_ = [dbus_out[i] for i in range(len(dbus_out))]
    return list_


def createUser(passwd, username):
    """
    根据用户名创建账户,并检查创建成功(创建普通用户)
    :param passwd: 用户密码
    :param username: 用户名
    :return:string
    """
    res = get_groups_detail()
    if username in res:
        logging.info('user账户名已存在，请删除后再创建')
        deleteUser(passwd, username)
        logging.info("删除{}完成".format(username))

    out = cmd_input(passwd,
                    dbus_iface="com.deepin.daemon.Accounts.CreateUser string:{} string:'' int32:0".format(username))
    logging.info(out)
    return out


def createUser2(passwd, username, type):
    """
    根据用户名创建账户,不对结果进行检查
    :param passwd:用户密码
    :param username:用户名
    :param type: type:1,系统用户，0普通用户
    :return: None
    """
    res = get_groups_detail()
    if username not in res:
        logging.info('创建测试账户')
        out = cmd_input(passwd,
                        dbus_iface="com.deepin.daemon.Accounts.CreateUser string:{} string:'' int32:{}".format(username,
                                                                                                               type))
        logging.info(out)
    else:
        pass


@checkword
def checkCreateUserStatus(username):
    """
    检查用户创建状态
    :param username: 用户名
    :return: True or False
    """
    res = get_groups_detail()
    if username in res:
        logging.info("检查账户 {} 创建成功".format(username))
        return True
    else:
        logging.info("检查账户 {} 创建失败".format(username))
        return False


def deleteUser(passwd, username):
    """
    删除指定账户
    :param passwd: 用户密码
    :param username: 用户名
    :return: None
    """
    res = get_groups_detail()
    if username in res:
        logging.info("删除{}账户".format(username))
        cmd_input(passwd, dbus_iface='com.deepin.daemon.Accounts.DeleteUser string:{} boolean:true'.format(username))
    else:
        logging.info("{}账户不存在，无需删除".format(username))


@checkword
def checkDeleteUserStatus(username):
    """
    检查根据用户名删除用户成功
    :param username: 用户名
    :return: True or False
    """
    res = get_groups_detail()
    if username not in res:
        logging.info("检查删除{}成功".format(username))
        return True
    else:
        logging.info("检查删除{}失败".format(username))
        return False


@checkword
def getGroups():
    """
    获取用户组的所有信息
    :return: True or False
    """
    time.sleep(2)
    res = get_groups_detail()
    logging.info(res)
    if res:
        logging.info("返回用户组的信息正常")
        return True
    else:
        logging.info("返回用户组的信息异常")
        return False


def get_groups_detail():
    """
    获取groups详细信息列表
    :return:list
    """
    property_obj = system_bus()
    dbus_out = property_obj.GetGroups()
    list_ = []
    for i in range(len(dbus_out)):
        t = re.findall(r'\S*', dbus_out[i])
        list_.append(t[0])
    return list_


@checkword
def getPresetGroups(mode):
    """
    根据账户类型获取用户组的信息
    :param mode:0 为普通用户，1 为管理员
    :return:True or False
    """
    time.sleep(2)
    property_obj = system_bus()
    dbus_out = property_obj.GetPresetGroups(mode)
    list_ = []
    for i in range(len(dbus_out)):
        t = re.findall(r'\S*', dbus_out[i])
        list_.append(t[0])
    logging.info(list_)
    if mode == 0:
        if 'sudo' not in list_:
            logging.info("获取普通用户信息成功")
            return True
        else:
            logging.info("获取普通用户信息失败")
            return False
    elif mode == 1:
        if 'sudo' in list_:
            logging.info("获取管理员用户信息成功")
            return True
        else:
            logging.info("获取管理员用户信息失败")
            return False


def getGuestUserName():
    """
    获取所有来宾用户名称列表
    :return:list
    """
    res = get_groups_detail()
    logging.info(res)
    user_list = []
    for i in range(len(res)):
        out = re.findall(r'guest\S*', res[i])
        if out:
            user_list.append(out[0])
    return user_list


def deleteAllGuestUser(passwd):
    """
    删除所有来宾用户
    :param passwd:用户密码
    :return: None
    """
    res = getGuestUserName()
    logging.info("来宾账户为: {}".format(res))
    if res:
        for item in res:
            logging.info("进行删除 {}".format(item))
            cmd_input(passwd, dbus_iface='com.deepin.daemon.Accounts.DeleteUser string:{} boolean:true'.format(item))
            logging.info("删除 {}完成".format(item))
    else:
        logging.info("来宾账户不存在，无需删除")


@checkword
def checkDeleteAllGuestUserStatus():
    """
    检查来宾账户全部删除成功
    :return:True or False
    """
    res = getGuestUserName()
    if not res:
        logging.info("来宾账户全部删除成功")
        return True
    else:
        logging.info("来宾账户全部删除失败")
        return False


@checkword
def findUserById(passwd, username):
    """
    通过新创建的用户id来查找用户
    :param passwd:用户密码
    :param username:用户名
    :return:True or False
    """
    out = createUser(passwd, username)
    user_path = out.split('\n')[-1]
    logging.info(user_path)
    id = re.findall(r'User(\d*)', user_path)[0]
    logging.info("新建账户id为：{}".format(id))
    property_obj = system_bus()
    dbus_out = property_obj.FindUserById(id)
    check_out = re.findall(r'User(\d*)', dbus_out)[0]
    logging.info("查找到的账户id为：{}".format(check_out))
    if id == check_out:
        logging.info("通过id查询账户成功")
        return True
    else:
        logging.info("通过id查询账户失败")
        return False


def findUserByName2(passwd, username):
    """
    通过用户id来查找用户
    :param passwd:用户密码
    :param username:用户名
    :return:string
    """
    property_obj = system_bus()
    dbus_out = property_obj.FindUserByName(username)
    check_out = re.findall(r'User(\S*)', dbus_out)[0]
    return check_out


@checkword
def findUserByName(passwd, username):
    """
    通过用户id来查找用户,并检查查找成功
    :param passwd:用户密码
    :param username:用户名
    :return:True or False
    """
    out = createUser(passwd, username)
    user_path = out.split('\n')[-1]
    logging.info(user_path)
    id = re.findall(r'User(\d*)', user_path)[0]
    logging.info("新建账户id为：{}".format(id))
    property_obj = system_bus()
    dbus_out = property_obj.FindUserByName(username)
    check_out = re.findall(r'User(\S*)', dbus_out)[0]
    logging.info("查找到的账户{} id为：{}".format(username, check_out))
    if id == check_out:
        logging.info("通过Name查询账户成功")
        return True
    else:
        logging.info("通过Name查询账户失败")
        return False


@checkword
def isPasswordValid(passwd, mode):
    """
    函数暂时未生效，会跟进
    :param passwd: 用户密码
    :param mode: valid or invalid
    :return:True or False
    """
    property_obj = system_bus()
    dbus_out = property_obj.IsPasswordValid(passwd)
    logging.info((list(dbus_out))[0])
    if mode == 'valid':
        if (list(dbus_out))[0]:
            logging.info("检查密码有效成功")
            return True
        else:
            logging.info("检查密码有效失败")
            return False
    elif mode == 'invalid':
        if not (list(dbus_out))[0]:
            logging.info("检查密码无效成功")
            return True
        else:
            logging.info("检查密码无效失败")
            return False


@checkword
def isUsernameValid(username, mode):
    """
    检查用户名是否有效
    :param username:用户密码
    :param mode:valid or invalid
    :return:True or False
    """
    property_obj = system_bus()
    dbus_out = property_obj.IsUsernameValid(username)
    logging.info((list(dbus_out))[0])
    if mode == 'valid':
        if (list(dbus_out))[0]:
            logging.info("检查用户名有效成功")
            return True
        else:
            logging.info("用户名已存在，检查用户名有效失败")
            return False
    elif mode == 'invalid':
        if not (list(dbus_out))[0]:
            logging.info("检查用户名无效成功")
            return True
        else:
            logging.info("检查用户名无效失败")
            return False


@checkword
def randUserIcon():
    """
    随机返回一个用户头像的文件绝对路径
    :return:True or False
    """
    time.sleep(2)
    icon_path = 'file:///var/lib/AccountsService/icons'
    property_obj = system_bus()
    dbus_out = property_obj.RandUserIcon()
    logging.info(dbus_out)
    if icon_path in dbus_out:
        logging.info("返回文件绝对路径正常")
        return True
    else:
        logging.info("返回文件绝对路径异常")
        return False


@checkword
def getGuestIcon():
    """
    获取来宾用户的图标绝对路径
    :return: True or False
    """
    time.sleep(2)
    property_obj = system_bus(iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Accounts', 'GuestIcon')
    logging.info(dbus_out)
    s = '/var/lib/AccountsService/icons/guest.png'
    if s in dbus_out:
        logging.info("获取来宾用户的图标绝对路径成功")
        return True
    else:
        logging.info("获取来宾用户的图标绝对路径失败")
        return False


def send_signal(passwd, username):
    """
    新建和删除用户（触发信号）
    :param passwd:用户密码
    :param username:用户名
    :return: None
    """
    logging.info("开始发送触发信号")
    logging.info("开始新建账户")
    createUser(passwd, username)
    logging.info("开始删除账户")
    deleteUser(passwd, username)


def signal_handler(*args, **kwargs):
    dbus_path0 = constant.dbus_path
    kwarg = str(kwargs)
    file_path = f"{dbus_path0}/account_signal.log"
    cmd = 'echo ' + kwarg + f'>> "{file_path}"'
    os.system(cmd)


def delGroup(passwd, group_name):
    """
    新建用户组
    :param passwd:用户密码
    :param group_name:用户名
    :return:None
    """
    logging.info("删除组{}".format(group_name))
    cmd = f'echo {passwd} | sudo -S groupdel {group_name}'
    (status, output) = getstatusoutput(cmd)
    logging.info(f"删除组命令返回值{output}")


def receive_signal():
    """
    接收信号
    :return: None
    """
    logging.info("启动监护线程，接收signal信号")
    bus = dbus.SystemBus()
    bus.add_signal_receiver(signal_handler, bus_name='com.deepin.daemon.Accounts', member_keyword='member')
    loop = GLib.MainLoop()
    loop.run()


@checkword
def check_signal():
    """
    检查信号接收是否成功
    :return: True or False
    """
    logging.info("开始检查接收信号内容是否正确")
    dbus_path0 = constant.dbus_path
    my_file = '{}/account_signal.log'.format(dbus_path0)
    loop = 10
    while loop:
        time.sleep(2)
        if os.path.exists(my_file):
            logging.info("收集信号完成")
            with open(my_file) as f:
                content = f.readlines()
            list_ = []
            for i in content:
                pattern = r'UserAdded|UserDeleted'
                t = re.findall(pattern, i)
                if t:
                    list_.append(t[0])
            logging.info("收集到的信号内容为：{}".format(list_))
            if 'UserAdded' and 'UserDeleted' in list_:
                logging.info("检查接收信号成功")
                return True
            else:
                logging.info("检查接收信号失败")
                return False
        else:
            logging.info("收集信号还没完成,继续等待")
            loop = loop - 1
    else:
        logging.info("等待超时，请重新收集")
        return False


def monitorSignals(passwd, username):
    """
    多线程实现信号触发，接收
    :param passwd:用户密码
    :param username:用户名
    :return:None
    """
    dbus_path0 = constant.dbus_path
    my_file = '{}/account_signal.log'.format(dbus_path0)
    if os.path.exists(my_file):
        os.remove(my_file)
        logging.info("删除已存在account_signal.log文件")

    threads = []

    my_thread1 = threading.Thread(target=receive_signal)
    threads.append(my_thread1)

    my_thread2 = threading.Thread(target=send_signal, args=(passwd, username))
    threads.append(my_thread2)

    my_thread1.setDaemon(True)

    for i in threads:
        i.start()
    time.sleep(5)
    check_signal()
    if os.path.exists(my_file):
        os.remove(my_file)
        logging.info("删除已存在account_signal.log文件")
