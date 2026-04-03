# -*- coding:utf-8 -*-
import os
import time
import logging
import subprocess

import dbus
import pexpect

from frame import constant


def execute_command_by_subprocess(command):
    p = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, encoding='utf-8')

    out = p.stdout.read()
    err = p.stderr.read()
    if err:
        return err
    else:
        return out


def root_execute_command_by_stdin(command, passwd):
    command = f'echo {passwd} | sudo -S {command}'
    logging.info(command)
    time.sleep(1)
    result = execute_command_by_subprocess(command)
    return result


def root_execute_command_by_expect(command, passwd):
    command = f'sudo {command}'
    logging.info(command)
    time.sleep(1)
    ret = pexpect.spawn(command)
    i = ret.expect(['sudo', pexpect.EOF, pexpect.TIMEOUT], timeout=10)
    if i == 0:
        ret.sendline(passwd)
        result = ret.read().decode(encoding="utf-8")
    else:
        b_content = ret.before
        result = str(b_content, encoding="utf-8", errors='ignore')

    return result.strip()


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


def get_dbus_interface(dbus_name=None, dbus_path=None, iface_name=None, dbus_type=None):
    if dbus_type == 'system':
        dbus_proxy = dbus.SystemBus()
    elif dbus_type == 'session':
        dbus_proxy = dbus.SessionBus()
    else:
        raise ValueError(f'')

    dbus_object = dbus_proxy.get_object(dbus_name, dbus_path)
    dbus_interface = dbus.Interface(dbus_object, dbus_interface=iface_name)
    return dbus_interface


def get_system_dbus_interface(dbus_name=None, dbus_path=None, iface_name=None):
    return get_dbus_interface(dbus_name, dbus_path, iface_name, 'system')


def get_session_dbus_interface(dbus_name=None, dbus_path=None, iface_name=None):
    return get_dbus_interface(dbus_name, dbus_path, iface_name, 'session')


def dbus_send(dbus_name=None, dbus_path=None, dbus_iface_method=None, dbus_type=None, passwd=None, use_root=True,
              time_out=50000):
    command = f'dbus-send --{dbus_type} --print-reply  --reply-timeout={time_out}' \
              f' --dest={dbus_name} {dbus_path} {dbus_iface_method}'
    logging.info(command)
    if use_root:
        if passwd is None:
            raise RuntimeError()
        time.sleep(1)
        result = root_execute_command_by_stdin(command, passwd)
        logging.info(f'result:\n{result}')
        return result
    else:
        result = execute_command_by_subprocess(command)
        logging.info(f'result:\n{result}')
        return result


def dbus_send_for_system(dbus_name=None, dbus_path=None, dbus_iface_method=None, passwd=None, use_root=True,
                         time_out=50000):
    time.sleep(5)  # 防止连续发送发生错误
    return dbus_send(dbus_name=dbus_name, dbus_path=dbus_path, dbus_iface_method=dbus_iface_method, dbus_type='system',
                     passwd=passwd, use_root=use_root, time_out=time_out)


def dbus_send_for_session(dbus_name=None, dbus_path=None, dbus_iface_method=None, passwd=None, use_root=True,
                          time_out=50000):
    time.sleep(5)  # 防止连续发送发生错误
    return dbus_send(dbus_name=dbus_name, dbus_path=dbus_path, dbus_iface_method=dbus_iface_method, dbus_type='session',
                     passwd=passwd, use_root=use_root, time_out=time_out)


class DbusMonitor:
    """
    dbus-monitor 接口
    使用步骤：
    1.实例化此类,调用start方法
    2.触发相关动作
    3.调用stop or parse
    """

    def __init__(self, interface, path, member, dbus_type):
        """
        :param interface: dbus接口名
        :param path: duus路径名
        :param member: 要监控的信号量
        :param dbus_type: session or system
        """
        self.dbus_type = 'session '
        self.interface = interface
        self.path = path
        self.member = member
        self.file = os.path.join(constant.dbus_path, f'{member}.txt')
        self.command = f"dbus-monitor --{dbus_type} type='signal',interface='{self.interface}'"
        self.f = None
        self.p = None
        self.is_kill = None
        logging.info(f'command:{self.command}')
        logging.info(f'file:{self.file}')
        if not os.path.exists(constant.dbus_path):
            os.makedirs(constant.dbus_path)

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


def start_monitor_signal(interface, path, member, dbus_type):
    dbus_monitor = DbusMonitor(interface, path, member, dbus_type)
    dbus_monitor.start()
    return dbus_monitor


def start_monitor_signal_for_session(interface, path, member):
    return start_monitor_signal(interface, path, member, 'session')


def start_monitor_signal_for_system(interface, path, member):
    return start_monitor_signal(interface, path, member, 'system')


def stop_monitor_signal(dbus_monitor: DbusMonitor):
    dbus_monitor.stop()


def parse_stop_monitor_signal(dbus_monitor: DbusMonitor):
    return dbus_monitor.parse()
