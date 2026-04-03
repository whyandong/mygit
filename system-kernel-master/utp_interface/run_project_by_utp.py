# coding:utf-8
import os
import sys
import json
import time
import ftplib
import zipfile
import logging
import datetime
import argparse

from urllib import request
from logging.handlers import RotatingFileHandler

file_dir_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(file_dir_path)


def run_project_by_utp_log():
    log_root_path = os.path.join(file_dir_path, 'utp_log',
                                 'run_project_by_utp_log')
    if not os.path.exists(log_root_path):
        os.makedirs(log_root_path)

    now = datetime.datetime.now()
    today_str = now.strftime('%Y_%m_%d %H_%M_%S_%f')

    date_token = today_str.split(' ')[0]
    time_token = today_str.split(' ')[1]
    log_file_name = f'{int(time.time())}.log'
    log_file_dir = os.path.join(log_root_path, date_token, time_token)
    log_file_path = os.path.join(log_file_dir, log_file_name)
    if not os.path.exists(log_file_dir):
        os.makedirs(log_file_dir)

    main_log = logging.getLogger()
    main_log.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(name)s %(asctime)s %(levelname)s %(filename)s(%(lineno)d)::%(funcName)s - %(message)s'
    )

    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)

    rotating_file_handler = RotatingFileHandler(log_file_path,
                                                maxBytes=10000000,
                                                encoding='utf-8')
    rotating_file_handler.setLevel(logging.DEBUG)
    rotating_file_handler.setFormatter(formatter)

    main_log.addHandler(stream_handler)
    main_log.addHandler(rotating_file_handler)


def parser_fun():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mark', dest='mark', nargs='*', default=[])
    parser.add_argument('-I',
                        '--ID',
                        dest='id',
                        type=str,
                        nargs='*',
                        default=[])
    parser.add_argument('-S',
                        '--source',
                        dest='source',
                        type=str,
                        nargs='?',
                        default=None)

    parser.add_argument(
        '-sla',
        '--save_log_address',
        dest='save_log_address',
        default="save_log::12345678::192.168.122.131::save_log")
    args = parser.parse_args()
    return args


def run_project(args):
    run_command = "python3 pytest_runner.py"
    if args.mark:
        run_command = f"{run_command} -m {' '.join(args.mark)}"

    if args.id:
        run_command = f"{run_command} -I {' '.join(args.id)}"

    if args.source:
        run_command = f"{run_command} -S {args.source}"

    logging.info(f'run_command: {run_command}')
    os.chdir(root_path)
    os.system(run_command)


def post_result(url, post_data):
    try:
        logging.info(f'待上传数据:{os.linesep}'
                     f'url:{url}{os.linesep}'
                     f'post_data:{post_data}')

        headers = {
            'Accept-Charset': 'utf-8',
            'Content-Type': 'application/json'
        }
        params = json.dumps(post_data).encode('utf8')

        req = request.Request(url, data=params, headers=headers, method='POST')
        response = request.urlopen(req)

        logging.info(f'response：{response.read().decode("utf-8")}')
        logging.info(f'{"=" * 5}连接成功{"=" * 5}')
    except Exception as e:
        logging.exception(e)
        logging.info(f'{"=" * 5}连接失败{"=" * 5}')


def zip_file(in_path, out_path):
    files_info = []
    for dir_name, sub_dirs, files in os.walk(in_path):
        files_info.extend([os.path.join(dir_name, file) for file in files])

    f = zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED)
    for file in files_info:
        f.write(file)
    # 调用了close方法才会保证完成压缩
    f.close()


def ftp_is_live(ftp_host, ftp_user, ftp_passwd):
    """
    探测ftp服务器是否能访问
    :param ftp_host: 主机名
    :param ftp_user: 用户名
    :param ftp_passwd: 密码
    :return: None
    """

    try:
        ftp = ftplib.FTP(host=ftp_host, user=ftp_user, passwd=ftp_passwd)
        time.sleep(2)
        ftp.close()
        logging.info('ftp服务器可以访问')
    except Exception as e:
        logging.exception(e)
        logging.info('ftp服务器不能访问')
    time.sleep(2)


def ftp_up(ftp_host, ftp_user, ftp_passwd, ftp_save_dir, file):
    now = datetime.datetime.now()
    today_str = now.strftime('%Y_%m_%d')

    ftp = ftplib.FTP(host=ftp_host, user=ftp_user, passwd=ftp_passwd)

    try:
        ftp.cwd(ftp_save_dir)
        logging.info(f"ftp_save_dir:{ftp_save_dir}已存在")
    except ftplib.error_perm:
        logging.info(f"ftp_save_dir:{ftp_save_dir}不存在，自动创建路径")
        for dir_name in ftp_save_dir.split('/'):
            if dir_name.strip():
                if dir_name not in ftp.nlst():
                    ftp.mkd(dir_name)
                    ftp.cwd(dir_name)
                else:
                    ftp.cwd(dir_name)

    if today_str not in ftp.nlst():
        logging.info(f"日期目录:{today_str}不存在，自动创建路径")
        ftp.mkd(today_str)
    else:
        logging.info(f"日期目录: {today_str}已存在")

    ftp.cwd(today_str)
    logging.info(f'开始将文件{file}上传文件到{os.path.join(ftp_save_dir, today_str)}下')

    buffer_size = 1024
    # 上传文件
    file_handler = open(file, "rb")
    ftp.storbinary(f"STOR {file}", file_handler, buffer_size)
    file_handler.close()
    logging.info("上传成功")
    ftp.close()


def save_log(args):
    now = datetime.datetime.now()
    today_str = now.strftime('%Y_%m_%d_%H_%M_%S_%f')

    pms_job_path = os.path.join(root_path, 'resource/pms/pms_job.json')
    utp_interface_path = os.path.join(root_path,
                                      'utp_interface/utp_interface.json')

    save_path = 'logs'
    project_log = os.path.join(root_path, 'log')
    file_with_time = f"{today_str}_{save_path}"
    file_with_time_zip = f"{file_with_time}.zip"

    logging.info(f"save_path: {save_path}")
    logging.info(f"project_log: {project_log}")
    logging.info(f"file_with_time: {file_with_time}")
    logging.info(f"file_with_time_zip: {file_with_time_zip}")

    ftp_info = args.save_log_address.split("::")
    ftp_info = [item.strip() for item in ftp_info if item.strip()]
    ftp_user = ftp_info[0]
    ftp_passwd = ftp_info[1]
    ftp_host = ftp_info[2]
    ftp_save_dir = ftp_info[3]

    logging.info(f"ftp_info: {ftp_info}")
    logging.info(f"ftp_user: {ftp_user}")
    logging.info(f"ftp_passwd: {ftp_passwd}")
    logging.info(f"ftp_host: {ftp_host}")
    logging.info(f"ftp_save_dir: {ftp_save_dir}")

    logging.info(f"探测ftp是否可以访问....")
    ftp_is_live(ftp_host, ftp_user, ftp_passwd)

    logging.info('读取run_id拼接日志保存路径')
    try:
        with open(utp_interface_path, 'r') as f:
            utp_interface_info = json.load(f)
            run_id = utp_interface_info["run_id"]
            ftp_save_dir = os.path.join(ftp_save_dir, run_id)
            logging.info('读取run_id拼接日志保存路径成功')
    except Exception as e:
        logging.info('读取run_id拼接日志保存路径失败')
        logging.exception(e)

    logging.info(f"开始收集log....")
    os.chdir(os.path.join(file_dir_path, 'utp_log'))
    os.system(f"rm -r {save_path}")
    os.system(f"mkdir -p {save_path}")
    os.system(f"cp -r {pms_job_path} {save_path}")
    os.system(f"cp -r {utp_interface_path} {save_path}")
    os.system(f"cp -r {project_log} {save_path}")
    os.system(f"cp -r 'set_pms_log' {save_path}")
    os.system(f"cp -r 'run_project_by_utp_log' {save_path}")
    os.system(f"cp -r 'set_utp_interface_log' {save_path}")
    os.system(
        f"cp -r {os.path.join(root_path, 'resource/tools/auto_envion_deploy/install_log')} {save_path}"
    )
    os.system(f'cp -r {save_path} {file_with_time}')
    time.sleep(1)

    logging.info(f"开始压缩{file_with_time}")
    try:
        zip_file(file_with_time, file_with_time_zip)
    except Exception as e:
        logging.info(f"压缩出错")
        logging.exception(e)

    time.sleep(1)

    logging.info(f"开始上传到{ftp_host}")
    try:
        ftp_up(ftp_host, ftp_user, ftp_passwd, ftp_save_dir,
               file_with_time_zip)
    except Exception as e:
        logging.exception(e)
        logging.info(f"上传出错")

    logging.info(f"关闭pms上传功能")
    os.chdir(file_dir_path)
    os.system(
        f"python3 set_pms.py -u http://10.20.42.241:3000/api/v1/zbox/result -p 0 -t 0"
    )
    logging.info(f"删除utp_interface.json")
    os.system(f"rm utp_interface.json")
    time.sleep(1)


def set_env():
    logging.info('设置XDG_RUNTIME_DIR：/run/user/1000')
    os.putenv('XDG_RUNTIME_DIR', '/run/user/1000')
    logging.info('设置accessibility：true')
    os.system(
        'gsettings set org.gnome.desktop.interface toolkit-accessibility true')
    logging.info('设置 QT_LINUX_ACCESSIBILITY_ALWAYS_ON：1')
    os.putenv('QT_LINUX_ACCESSIBILITY_ALWAYS_ON', '1')
    logging.info('设置 QT_ACCESSIBILITY：1')
    os.putenv('QT_ACCESSIBILITY', '1')
    logging.info('设置 DISPLAY：:0')
    os.putenv('DISPLAY', ':0')


def run():
    # url = ""
    result_dict = {"pass": 0, "fail": 0, "blocked": 0}

    post_data = {
        "device_id": "",
        "task_id": "",
        "step_id": "",
        "status": "",
        "msg": "",
        "data": result_dict
    }

    utp_interface_info = os.path.join(file_dir_path, 'utp_interface.json')
    result_file_path = os.path.join(root_path, 'log/result.json')

    logging.info('\n\n')
    logging.info(f"{'=' * 50}======={'=' * 50}")
    logging.info(f"{'=' * 50}设置环境变量{'=' * 50}")
    set_env()
    logging.info(f"{'=' * 50}设置环境变量{'=' * 50}")
    logging.info(f"{'=' * 50}======={'=' * 50}")
    logging.info('\n\n')

    logging.info('\n\n')
    logging.info(f"{'=' * 50}======={'=' * 50}")
    logging.info(f"{'=' * 50}检查数据{'=' * 50}")
    try:
        args = parser_fun()
        logging.info(f'参数解析执行成功')
    except Exception as e:
        logging.info(f'参数解析执行错误')
        logging.exception(e)
        raise RuntimeError(f'参数解析执行错误')

    try:
        ftp_info = args.save_log_address.split("::")
        ftp_info = [item.strip() for item in ftp_info if item.strip()]
        ftp_user = ftp_info[0]
        ftp_passwd = ftp_info[1]
        ftp_host = ftp_info[2]
        ftp_save_dir = ftp_info[3]
        logging.info(f'log保存参数解析成功')

    except Exception as e:
        logging.info(f'log保存参数解析出错')
        logging.exception(e)
        raise RuntimeError(f'log保存参数解析出错')

    # 读取utp_interface.json
    try:
        logging.info('读取utp_interface.json')
        with open(utp_interface_info, 'r') as f:
            utp_interface_info = json.load(f)
            post_data["device_id"] = utp_interface_info["device_id"]
            post_data["task_id"] = utp_interface_info["task_id"]
            post_data["step_id"] = utp_interface_info["step_id"]
            url = utp_interface_info["url"]

        logging.info('读取utp_interface.json成功')
    except Exception as e:
        logging.info(f'读取接口文件失败{utp_interface_info}')
        logging.info(f'无法上传结果')
        logging.exception(e)
        time.sleep(5)
        save_log(args)
        raise RuntimeError(f'读取接口文件失败{utp_interface_info}')

    logging.info(f"{'=' * 50}检查数据{'=' * 50}")
    logging.info(f"{'=' * 50}======={'=' * 50}")
    logging.info('\n\n')

    # 执行测试
    logging.info('\n\n')
    logging.info(f"{'=' * 50}======={'=' * 50}")
    logging.info(f"{'=' * 50}执行测试{'=' * 50}")
    try:
        logging.info('执行测试')
        run_project(args)
        logging.info('执行测试完成')

    except Exception as e:
        logging.info('执行测试失败')
        logging.exception(e)
        post_data["status"] = '3'
        post_data["msg"] = str(e)
        post_data["data"] = result_dict
        save_log(args)
        post_result(url, post_data)
        sys.exit(0)

    logging.info(f"{'=' * 50}执行测试{'=' * 50}")
    logging.info(f"{'=' * 50}======={'=' * 50}")
    logging.info('\n\n')

    # 获取结果
    logging.info('\n\n')
    logging.info(f"{'=' * 50}======={'=' * 50}")
    logging.info(f"{'=' * 50}获取结果{'=' * 50}")
    try:
        os.chdir(file_dir_path)
        os.system(f"cp {result_file_path} 'utp_log/result.json'")
        result_file_path = 'utp_log/result.json'
        with open(result_file_path, 'r') as f:
            info = json.load(f)

        for item in info:
            res = info[item]["result"]
            result_dict[res] += 1

        post_data["status"] = '0'
        post_data["msg"] = '运行结束'
        post_data["data"] = result_dict
        logging.info('获取结果成功')
        save_log(args)
        post_result(url, post_data)

    except Exception as e:
        logging.info('获取结果出错')
        logging.exception(e)
        post_data["status"] = '3'
        post_data["msg"] = '获取结果出错'
        save_log(args)
        post_result(url, post_data)

    logging.info(f"{'=' * 50}获取结果{'=' * 50}")
    logging.info(f"{'=' * 50}======={'=' * 50}")
    logging.info('\n\n')


if __name__ == "__main__":
    run_project_by_utp_log()
    run()
