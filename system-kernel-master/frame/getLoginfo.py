#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
from frame import constant
import subprocess
import logging

report_dir = constant.dir_name
resoure_path = constant.resoure_path
dbus_path = os.path.join(resoure_path, 'dbus')


def excute_cmd(cmd):
    '''
    执行cmd命令
    '''
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, encoding='utf-8')

    outMsg = p.stdout.read()
    errMsg = p.stderr.read()
    if errMsg:
        return errMsg
    else:
        return outMsg


def getLastestReport(report_dir=report_dir):
    '''
    获取最新测试报告路径
    :param report_dir:
    :return:
    '''
    lists = os.listdir(report_dir)
    lists.sort(key=lambda fn: os.path.getmtime(report_dir + '/' + fn))
    # logging.info("the lastest report is "+lists[-1])
    file_path = os.path.join(report_dir, lists[-1])
    # print(file_path)
    return file_path


def getLastestHtml():
    '''
    获取最新HTML
    :param report_dir:
    :return:
    '''
    file_path = getLastestReport()
    for file in os.walk(file_path):
        for i in range(len(file[-1])):
            if '.html' in file[-1][i]:
                html0 = file[-1][i]
        html_file = os.path.join(file_path, html0)
        # logging.info(html_file)
        return html_file


def getLastestLog():
    '''
    获取最新log
    :param report_dir:
    :return:
    '''
    file_path = getLastestReport()
    for file in os.walk(file_path):
        for i in range(len(file[-1])):
            if '.log' in file[-1][i]:
                log0 = file[-1][i]
        log_file = os.path.join(file_path, log0)
        # logging.info(log_file)
        return log_file


def html_template():
    '''
    html模板
    :return:
    '''
    module_version = excute_cmd("dpkg -l | grep dde-daemon | awk '{ if (\"dde-daemon\" == $2) print $2\" \" $3 }'")
    dde_daemon_version = excute_cmd("dpkg -l | grep dde-daemon | awk '{ if (\"dde-daemon\" == $2) print $2\" \" $3 }'")
    startdde_version = excute_cmd("dpkg -l | grep startdde | awk '{ if (\"startdde\" == $2) print $2\" \" $3 }'")
    dde_api_version = excute_cmd("dpkg -l | grep dde-api | awk '{ if (\"dde-api\" == $2) print $2\" \" $3 }'")
    log_file = getLastestLog()
    with open(log_file, 'r') as file:
        info = file.read()
        start_info = re.findall(r'(\S*)', info)
        start_time = start_info[0] + ' ' + start_info[2]
        dural_time = re.findall(r'运行时间:\s(\S*)', info)[0]
        total_case = re.findall(r'共计执行用例数量：(\d*)', info)[0]
        pass_case = re.findall(r'执行成功用例数量：(\d*)', info)[0]
        fail_case = re.findall(r'执行失败用例数量：(\d*)', info)[0]
        error_case = re.findall(r'产生异常用例数量：(\d*)', info)[0]
        pass_rate = (int(pass_case) / int(total_case)) * 100
        fail_rate = (int(fail_case) / int(total_case)) * 100

    return '''
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <meta charset="utf-8">
    <title>DbusReport</title>
    <style>
        body {
            background-color:#f2f2f2;
            color:#333;
            margin: 0 auto;
            width: 960px;
        }
        #summary {
            width: 960px;
            margin-bottom: 20px;
        }
        #summary th {
            background-color: skyblue;
            padding: 4px 8px;
        }
        #summary td {
          background-color: lightblue;
          text-align: center;
          padding: 4px 8px;
        }
        .details {
            width: 960px;
            margin-bottom: 20px;
        }
        .details th {
            background-color: skyblue;
            padding: 5px 12px;
        }
        .details td {
            background-color: lightblue;
            padding: 5px 12px;
        }
    </style>
</head>
<body>
<h1 style="text-align: center;"><b><big> Test Report </big></b></h1>
<h2><b>Summary</b></h2>
<table id="summary">
    <tr>
        <th>dde_daemon_version</th>
        <td colspan="1"><b>%s</b></td>
    </tr>
    <tr>
        <th>dde_api_version</th>
        <td colspan="1"><b>%s</b></td>
    </tr>
    <tr>
        <th>startdde_version</th>
        <td colspan="1"><b>%s</b></td>
    </tr>
    <tr>
        <th>开始时间</th>
        <td colspan="1"><b>%s</b></td>
    </tr>
    <tr>
        <th>运行时间</th>
        <td colspan="1"><b>%s</b></td>
    </tr>
    <tr>
        <th>共计执行用例数量</th>
        <td colspan="1"><b>%s</b></td>
    </tr>
    <tr>
        <th>执行成功用例数量</th>
        <td colspan="1"><b>%s</b></td>
    </tr>
    <tr>
        <th>执行失败用例数量</th>
        <td colspan="1"><b>%s</b></td>
    </tr>
    <tr>
        <th>产生异常用例数量</th>
        <td colspan="1"><b>%s</b></td>
    </tr>
    <tr>
        <th>测试通过率</th>
        <td colspan="1"><b>%.2f%%</b></td>
    </tr>
    <tr>
        <th>测试失败率</th>
        <td colspan="1"><b>%.2f%%</b></td>
    </tr>
</table>
</body>
</html>
        ''' % (
        dde_daemon_version, dde_api_version, startdde_version, start_time, dural_time, total_case, pass_case, fail_case,
        error_case, pass_rate, fail_rate)


def get_content():
    '''
    获取邮件发送内容
    '''
    filename = '{}/html123.txt'.format(dbus_path)
    filename_temp = html_template()
    with open(filename, 'w') as f:
        f.write(filename_temp)
    with open(filename, 'r') as f:
        content = f.read()
    return content


if __name__ == "__main__":
    get_content()
