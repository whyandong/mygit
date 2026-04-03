# -*- coding: utf-8 -*-
import os
from frame import constant, common
import time
from datetime import date
from subprocess import getstatusoutput


def save_report_history():
    """
    处理history文件, allure生成趋势报告
    :return:None
    """
    history_path = os.path.join(constant.allure_report_path, 'history')

    if os.path.exists(constant.allure_results_path):
        os.system(f'rm -r {constant.allure_results_path}')
        os.makedirs(constant.allure_results_path)

    if os.path.exists(history_path):
        common.execute_command(
            f'cp -r {history_path} {constant.allure_results_path}')


def save_report_local():
    """
    将本地 allure_report文件保存至项目平级目录, 用于分析日志
    :return:None
    """
    today = date.today()
    local_report_path = os.path.join(constant.report_path, f'{today}')
    dbus_report_path = os.path.join(
        os.path.join(constant.report_path, f'{today}'), 'defender')

    current_time = time.strftime("%H-%M-%S")
    current_time_path = os.path.join(dbus_report_path, f'{current_time}')

    if os.path.exists(dbus_report_path):
        if os.path.exists(current_time_path):
            cmd = f'cp {constant.allure_report_path} -R {current_time_path}'
            status, output = getstatusoutput(cmd)
            if status == 0:
                print("报告copy成功")
                return local_report_path
            else:
                print("报告copy失败")
        else:
            os.makedirs(current_time_path)
            cmd = f'cp {constant.allure_report_path} -R {current_time_path}'
            status, output = getstatusoutput(cmd)
            if status == 0:
                print("报告copy成功")
                return local_report_path
            else:
                print("报告copy失败")
    else:
        os.makedirs(current_time_path)
        if os.path.exists(constant.allure_report_path):
            cmd = f'cp {constant.allure_report_path} -R {current_time_path}'
            status, output = getstatusoutput(cmd)
            if status == 0:
                print("报告copy成功")
                return local_report_path
            else:
                print("报告copy失败")

        else:
            print("原始报告文件不存在")


def scp_report(local_report_path):
    """
    将本地报告传至远程服务器
    """
    cmd = f"sshpass -p '1' scp -r {local_report_path} uos@10.20.52.242:~/UTP_report/"
    print(cmd)
    status, output = getstatusoutput(cmd)
    if status == 0:
        print("报告传输成功")
    else:
        print("报告传输失败")
        print(output)


if __name__ == '__main__':
    report = save_report_local()
    scp_report(report)
