# coding:utf-8
import os
import logging
import subprocess

from frame import constant


def excute_cmd(cmd):
    """
    执行cmd命令,输出内容
    :param cmd:输入的命令
    :return:命令执行内容输出
    """
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, encoding='utf-8')
    out_msg = p.stdout.read()
    err_msg = p.stderr.read()
    if err_msg:
        return err_msg
    else:
        return out_msg


def get_ip():
    command = 'ifconfig'
    content_list = os.popen(command).readlines()
    for content in content_list:
        content = content.strip()
        if content.startswith('inet') and not content.startswith('inet6'):
            _ = content.split(' ')
            ip = _[1]
            if ip != '127.0.0.1':
                return ip
    else:
        return 'N/A'


def get_dde_environment():
    """
    获取dde environment参数
    :return: None
    """
    allure_results_path = constant.allure_results_path
    environment_file = os.path.join(allure_results_path, "environment.properties")
    uos_version = '20 Professional'
    device_ip = get_ip()
    dde_daemon_version = excute_cmd("dpkg -l |grep dde-daemon| awk '{if(\"dde-daemon\"==$2)print $3}'")
    dde_api_version = excute_cmd("dpkg -l |grep dde-api | awk '{if(\"dde-api\"==$2)print $3}'")
    startdde_version = excute_cmd("dpkg -l |grep startdde | awk '{if(\"startdde\"==$2)print $3}'")
    lastore_daemon_version = excute_cmd("dpkg -l |grep lastore-daemon | awk '{if(\"lastore-daemon\"==$2)print $3}'")

    info_dict = {'UOS_VERSION': uos_version,
                 'DEVICE_IP': device_ip,
                 'DDE_DAEMON_VERSION': dde_daemon_version,
                 'DDE_API_VERSION': dde_api_version,
                 'START_DDE_VERSION': startdde_version,
                 'LASTORE_DAEMON': lastore_daemon_version
                 }
    logging.info(info_dict)

    with open(environment_file, "w") as f:
        for key in info_dict:
            logging.info(f'{key}: {info_dict[key].strip()}')
            f.write(f'{key} = {info_dict[key].strip()}\n')

    categories_file = os.path.join(constant.resoure_path, 'categories.json')
    excute_cmd(f'cp {categories_file} {allure_results_path}')
