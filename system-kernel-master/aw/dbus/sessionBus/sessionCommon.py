# -*- coding: utf-8 -*-
import os
import time
import logging
import subprocess

import pexpect
import dbus

from frame import constant


def session_bus(dbus_name=None, dbus_path=None, iface_name=None):
    session_bus = dbus.SessionBus()
    session_obj = session_bus.get_object(dbus_name, dbus_path)
    property_obj = dbus.Interface(session_obj, dbus_interface=iface_name)
    return property_obj


def excute_cmd(cmd):
    """
    执行cmd命令
    :param cmd:输入的命令
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


def pexpect_cmd(passwd, cmd):
    """
    sudo命令密码交互输入
    :param passwd:系统用户名密码
    :param cmd:执行的cmd命令
    :return:命令输出结果
    """
    ret = pexpect.spawn(cmd)
    i = ret.expect('sudo', timeout=5)  # i=0,匹配成功
    if i == 0:
        ret.sendline(passwd)
    out = ret.read().decode(encoding="utf-8")
    logging.info(out)
    return out


def cmd_input(passwd, dbus_name=None, dbus_path=None, dbus_iface_method=None):
    """
    dbus-send模式进行接口测试，sudo输入密码
    :param passwd: 密码
    :param dbus_name: 接口名
    :param dbus_path: 接口路径
    :param dbus_iface_method: 接口传入对应的方法和参数
    :return: string
    """
    cmd = 'sudo dbus-send --session --print-reply  --dest={} {} {}'.format(dbus_name, dbus_path, dbus_iface_method)
    logging.info(cmd)
    time.sleep(1)
    ret = pexpect.spawn(cmd)
    i = ret.expect(['sudo', pexpect.EOF, pexpect.TIMEOUT], timeout=10)
    if i == 0:
        ret.sendline(passwd)
        result = ret.read().decode(encoding="utf-8")
    else:
        b_content = ret.before
        result = str(b_content, encoding="utf-8", errors='ignore')

    result = result.strip()
    logging.info(result)
    return result


class DbusMonitor:
    """
    dbus-monitor 接口
    使用步骤：
    1.实例化此类,调用start方法
    2.触发相关动作
    3.调用stop or parse
    """

    def __init__(self, interface, path, member):
        """
        :param interface: dbus接口名
        :param path: duus路径名
        :param member: 要监控的信号量
        """
        self.dbus_type = 'session '
        self.interface = interface
        self.path = path
        self.member = member
        self.file = os.path.join(constant.dbus_path, f'{member}.txt')
        self.command = f"dbus-monitor --session type='signal',interface='{self.interface}'"
        self.f = None
        self.p = None
        self.is_kill = None
        logging.info(f'command:{self.command}')
        logging.info(f'file:{self.file}')

    def start(self):
        if os.path.exists(self.file):
            os.remove(self.file)
            time.sleep(0.5)
        self.f = open(self.file, mode='w', encoding='utf-8')
        time.sleep(0.5)
        self.p = subprocess.Popen(self.command, shell=True, stdout=self.f)
        time.sleep(0.5)

    def _get_pid(self):
        command = 'ps -aux | grep dbus-monitor'
        p = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, encoding='utf-8')
        out = p.stdout.read()
        pid_list = []
        if out:
            out = out.strip()
            content_list = out.split('\n')
            for i in content_list:
                _ = [item for item in i.split(' ') if item]
                pid_list.append(_[1])

        return pid_list

    def stop(self):
        if self.p and self.is_kill is None:
            logging.info(f'杀死所有监听进程')
            self.p.kill()
            for pid in self._get_pid():
                command = f'kill -9 {pid}'
                logging.info(command)
                os.system(command)
                time.sleep(0.5)
                # os.kill(int(pid), signal.SIGKILL)
            self.is_kill = True
            time.sleep(0.5)

        if self.f and self.f.closed is False:
            self.f.close()
            time.sleep(0.5)
            logging.info('file is closed')

    def parse(self) -> str:
        """
        从文件中解析出要获取的信号量对应的一段信息
        :return: str
        """
        self.stop()
        end = None
        start = None
        with open(self.file, 'r', encoding='utf-8') as f:
            line_list = f.readlines()
            list_len = len(line_list)
            if list_len > 0:
                end = list_len

            for i in range(list_len - 1, -1, -1):
                text = line_list[i]
                logging.info(text)
                if text.startswith('signal'):
                    if f'path={self.path};' in text and \
                            f'interface={self.interface};' and \
                            f'member={self.member}' in text:
                        start = i
                        break
                    else:
                        end = i
            else:
                logging.info('未获取到信号信息')

        logging.info(f'start:{start},end:{end}')
        if end is not None and start is not None:
            result = ''.join(line_list[start:end])
            result = result.strip()
            logging.info(f'result:\n{result}')
            return result
        else:
            return ''


def install_deb(passwd, deb_path):
    """
    安装deb包
    :param passwd: 帐号密码
    :param deb_path: deb包路径
    :return: str:安装日志
    """
    commad = f'sudo dpkg -i {deb_path}'
    ret = pexpect.spawn(commad)
    i = ret.expect('sudo', timeout=5)  # i=0,匹配成功
    if i == 0:
        ret.sendline(passwd)
    out = ret.read().decode(encoding="utf-8")
    logging.info(out)
    return out


def remove_deb(passwd, app_name):
    """
    卸载deb包
    :param passwd: 帐号密码
    :param app_name: 应用名
    :return: str:卸载日志
    """
    commad = f'sudo dpkg -r {app_name}'
    ret = pexpect.spawn(commad)
    i = ret.expect('sudo', timeout=5)  # i=0,匹配成功
    if i == 0:
        ret.sendline(passwd)
    out = ret.read().decode(encoding="utf-8")
    logging.info(out)
    return out
