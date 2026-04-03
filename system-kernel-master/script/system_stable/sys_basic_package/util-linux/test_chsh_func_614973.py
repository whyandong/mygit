#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          614973
# @Test Description:
# @Test Condition:
# @Test Step:            1.获取udisks规则基线数据 2.获取系统udisks规则数据,与步骤1的结果对比
# @Test expect Result:   1.正常获取 2.对比无差异
# @Test Remark:
# @Author:  夏曙_ut000220
# @Date: 2022/5/24
# *****************************************************

import sys
import pytest
import logging
import subprocess
from frame.common import system_kernel_log_cap


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enablle stage !")
    yield
    cmd = 'echo 1 | chsh -s /bin/bash'
    subprocess.run(cmd,
                   shell=True,
                   stdin=subprocess.PIPE,
                   stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE,
                   encoding='utf-8')
    logging.info("this is env disable stage !")


def test_chsh_func_614973():
    logging.info("step1: 查看当前用户的默认shell")
    cmd1 = r"cat /etc/passwd | grep uos | awk -F: '{print $NF}'"
    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    shell_default = p001.stdout.read().strip()

    logging.info("step2: 获取系统支持的shell列表")
    cmd2 = r"cat /etc/shells | grep -v '^#'"
    p002 = subprocess.Popen(cmd2,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    shells_lst = p002.stdout.read().strip().split("\n")

    logging.info("step3: 修改当前用户的默认shell")
    shell_changed_err_times = 0
    change_time = 0
    for shell in shells_lst:
        change_time += 1
        logging.info("the " + str(change_time) + " time to change shell:")
        cmd3 = 'echo 1 | chsh -s ' + shell
        subprocess.run(cmd3,
                       shell=True,
                       stdin=subprocess.PIPE,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,
                       encoding='utf-8')

        cmd4 = r"cat /etc/passwd | grep uos | awk -F: '{print $NF}'"
        p004 = subprocess.Popen(cmd4,
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                encoding='utf-8')
        shell_changed = p004.stdout.read().strip()
        logging.info(shell)
        logging.info(shell_changed)

        if shell == shell_changed:
            logging.info("shell修改成功")
        else:
            shell_changed_err_times += 1
            return shell_changed_err_times

    logging.info(shell_changed_err_times)
    if shell_default == "/bin/bash" and shell_changed_err_times == 0:
        assert True
    else:
        logging.error("用户默认shell检查或chsh修改当前用户默认shell失败，请检查")
        logging.debug("用户默认shell：" + shell_default)
        logging.debug("系统支持shell列表如下：")
        logging.debug(shells_lst)
        logging.debug("修改系统默认shell失败次数：" + str(shell_changed_err_times))
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
