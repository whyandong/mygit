#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          629336
# @Test Description:      检查系统自启服务运行状态检查是否有inactive的自启动服务
# @Test Condition:
# @Test Step:           1.过滤出所有的loaded且inactive状态的服务，判断该部分服务是否存在自启动的服务。（如果type=oneshot，且没有定义RemainAfterExit=yes，则认为正常忽略）
# @Test expect Result:  1.自启动服务中没有启动失败的服务（loaded+inactive），以下已经确认和评审的除外：rsync.service，getty @ tty1.service
# @Test Remark:
# @Author:  夏曙_ut000220
# @Date:    2022/5/10
# *****************************************************
from copy import deepcopy
import sys
import pytest
import logging

from frame.common import execute_command, system_kernel_log_cap


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enable stage !")
    yield
    logging.info("this is env disable stage !")


def test_enabled_service_inactive_check_629336():

    logging.info("step1:过滤出所有自启服务中的loaded且inactive状态的服务：")
    cmd1 = "systemctl list-units --all | grep service | grep loaded | grep inactive | awk '{print $1}'"
    service_loaded_inactive_lst = (execute_command(cmd1)).split("\n")
    remove_lst = [
        "rsync.service", "getty@tty1.service", "systemd-fsck-root.service",
        "uos-reporter.service"
    ]
    logging.debug(f"当前获取到的未激活服务有{service_loaded_inactive_lst}")
    service_loaded_inactive_lst = list(set(service_loaded_inactive_lst) - set(remove_lst))

    service_loaded_inactive_lst_new = deepcopy(service_loaded_inactive_lst)
    for service in service_loaded_inactive_lst_new:
        get_enabled_state = "systemctl is-enabled " + service
        get_type = "systemctl cat " + service + "| grep Type | awk -F= '{print $2}'"
        get_remain_after_exit = "systemctl cat " + service + "| grep RemainAfterExit | awk -F= '{print $2}'"

        is_enabled = execute_command(get_enabled_state).strip()
        type = execute_command(get_type).strip()
        remain_after_exit = execute_command(get_remain_after_exit).strip()

        if "enabled" in is_enabled:
            if type == "oneshot" and (remain_after_exit == "no"
                                      or remain_after_exit == ""):
                service_loaded_inactive_lst.remove(service)
        else:
            service_loaded_inactive_lst.remove(service)

    if len(service_loaded_inactive_lst) == 0:
        assert True
    else:
        logging.error("系统存在" + str(len(service_loaded_inactive_lst)) +
                      "个启动异常的自启服务：")
        logging.error(service_loaded_inactive_lst)
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
