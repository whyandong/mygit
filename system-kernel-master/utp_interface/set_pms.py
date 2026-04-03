# coding:utf-8
import os
import sys
import json
import time
import logging
import datetime

import argparse

from logging.handlers import RotatingFileHandler

file_dir_path = os.path.dirname(os.path.abspath(__file__))  # 文件所在路径
root_path = os.path.dirname(file_dir_path)  # 文件所在路径

parser = argparse.ArgumentParser()
parser.add_argument('-u',
                    '--baseurl',
                    dest='baseurl',
                    default="http://10.0.10.200:3000/api/v1")
parser.add_argument('-p',
                    '--productid',
                    dest='product_id',
                    type=int,
                    default=0)
parser.add_argument('-t', '--taskid', dest='task_id', type=int, default=0)
args = parser.parse_args()

json_file_path = os.path.join(root_path, 'resource/pms/pms_job.json')


def set_pms_log():
    log_root_path = os.path.join(file_dir_path, 'utp_log', 'set_pms_log')
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


def pms_args2json(baseurl, product_id, task_id):
    logging.info(f'baseurl:{baseurl}{os.linesep}'
                 f'product_id:{product_id}{os.linesep}'
                 f'task_id:{task_id}{os.linesep}')

    with open(json_file_path, mode="w", encoding="utf-8") as j:
        json.dump(
            {
                'baseurl': baseurl,
                'product_id': product_id,
                'task_id': task_id
            }, j)


if __name__ == "__main__":
    try:
        set_pms_log()
        pms_args2json(args.baseurl, args.product_id, args.task_id)
    except Exception as e:
        logging.exception(e)
        raise e
