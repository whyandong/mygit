#!/usr/bin/python
# -*- coding: utf-8 -*- #

import os
import sys
import time
import subprocess
import json
import csv
from collections import namedtuple

json_template = {
    "appName": "project_name",
    "source": "CRPCI",
    "arch": "",
    "buildLocaltion": "wuhan",
    "checkName": "ATtest",
    "checkResult": "0,0,0%",
    "checkStatus": "success",
    "buildURL": "jenkins构建地址",
    "startTime": 1111111,
    "endTime": 1111111,
    "version": "1050"
}

project_array = ["system", "cve", "linglong", "secirity"]
all_case = []
app = sys.argv[1]


def filter_case():
    t_list = []
    with open("case_list.csv", "r", encoding="utf-8") as f:
        f_csv = csv.reader(f)
        # 根据表头生成结构体,并根据传入模块名称获取所需测试用例
        Row = namedtuple('Row', next(f_csv))
        for each_row in f_csv:
            row_info = Row(*each_row)
            # print(row_info.是否跳过)
            # print(row_info.用例模块)
            # print(each_row)
            if "是" in row_info.是否跳过 or app not in row_info.用例模块:
                continue
            else:
                # print(row_info.用例ID)
                t_list.append(row_info.用例ID)
    with open("execute.txt", "w", encoding="utf-8") as fd:
        for line in t_list:
            # print(line)
            fd.write(line + "\n")
        fd.close()


def set_env():
    os.environ['DBUS_SESSION_BUS_ADDRESS'] = "unix:path=/run/user/1000/bus"
    os.environ['XDG_RUNTIME_DIR'] = "/run/user/1000"
    os.environ['DISPLAY'] = ":0"
    os.environ['USER'] = ":uos"
    os.environ['QT_LINUX_ACCESSIBILITY_ALWAYS_ON'] = "1"
    os.environ['QT_ACCESSIBILITY'] = "1"
    os.system(
        "gsettings set org.gnome.desktop.interface toolkit-accessibility true")


def execute_dbus_job(project_name):
    command = "python3 pytest_runner.py -md " + project_name
    os.system(command)


def analysis_dbus_report():
    pwd = os.getcwd()
    csv_path = pwd + '/allure-report/data/suites.csv'
    print(csv_path)
    passed_command = 'grep -w passed %s | wc -l' % csv_path
    failed_command = 'grep -w failed %s | wc -l' % csv_path
    broken_command = 'grep -w broken %s | wc -l' % csv_path
    passed = subprocess.getoutput(passed_command)
    failed = subprocess.getoutput(failed_command)
    broken = subprocess.getoutput(broken_command)
    return passed, failed, broken


def analysis_report(project_name, json_template, start_time, end_time):
    dbus_passed = int(analysis_dbus_report()[0])
    dbus_failed = int(analysis_dbus_report()[1])
    dbus_broken = int(analysis_dbus_report()[2])
    dbus_total = dbus_passed + dbus_failed + dbus_broken
    report_failed_rate = str('%.1f' % (dbus_failed / dbus_total * 100)) + '%'
    data = '%s,%s,%s' % (str(dbus_failed), str(dbus_total), report_failed_rate)
    if project_name == "deepin-authentication":
        project_name == "deepin-authenticate"
    subproject_version = subprocess.getoutput(
        f"apt list {project_name}" +
        "| awk -F ' ' '{if($0~\"已安装\")print $2}'").split('\n')[-1]
    json_template["appName"] = project_name
    json_template["checkResult"] = data
    json_template["startTime"] = start_time
    json_template["endTime"] = end_time
    json_template["version"] = subproject_version
    json_tem = json.dumps(json_template)
    print(json_tem)
    file_name = project_name + '_at.json'
    with open(file_name, 'w') as f:
        f.write(json_tem)


if __name__ == "__main__":
    set_env()
    filter_case()
    if sys.argv[1] in project_array:
        start_time = int(time.time())
        execute_dbus_job(sys.argv[1])
        end_time = int(time.time())
        analysis_report(sys.argv[1], json_template, start_time, end_time)
    else:
        print("please enter correct project name")
