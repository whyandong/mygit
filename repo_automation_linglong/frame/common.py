# -*- coding: utf-8 -*-
import subprocess


def execute_command(command):
    """
    执行终端命令,输出内容
    :param command:输入的命令
    :return:命令执行内容输出
    """
    p = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, encoding='utf-8')
    out_msg = p.stdout.read()
    err_msg = p.stderr.read()
    return out_msg
    # if err_msg:
    #     return err_msg
    # else:
    #     return out_msg