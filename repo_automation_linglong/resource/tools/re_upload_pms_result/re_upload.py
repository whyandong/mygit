# -*- coding: utf-8 -*-
import os
import json
import logging
from urllib import request, parse


def send_result2pms(script_path, info_dict):
    script = os.path.split(script_path)[1].split('.')[0]
    with open('pms_job.json', 'r', encoding='utf-8') as f, open('name2id.json', 'r', encoding='utf-8') as f2:
        base_info = json.load(f)
        pms_case_id = json.load(f2).get(script, "")

    if not pms_case_id:
        logging.info(f'{"=" * 5}未查到用例{script_path}对应的pms编号,请及时刷新resource/pms/name2id.json文件内容{"=" * 5}')

    if base_info['task_id'] is 0 or base_info['product_id'] is 0:
        logging.info(f'task_id：{base_info["task_id"]},product_id：{base_info["product_id"]}')
        logging.info(f'不上传测试结果到pms')

    logging.info(f'script_path：{script_path}')
    logging.info(f'info_dict：{info_dict}')

    post_data = {'product_id': base_info['product_id'],
                 'task_id': base_info['task_id'],
                 'case_id': pms_case_id,
                 'result': info_dict['result'],
                 'reals': info_dict['longrepr'],
                 'test_type': base_info['test_type'],
                 'testtask_name': base_info['testtask_name'],
                 'area': base_info['area'],
                 'user_name': base_info['user_name']}

    logging.info(f'上传{pms_case_id}测试结果到pms')
    logging.info(f'post_data：{post_data}')
    try:
        response = request.urlopen(base_info['baseurl'],
                                   data=parse.urlencode(post_data).encode('utf-8'))
        logging.info(f'response：{response.read().decode()}')
        logging.info(f'{"=" * 5}连接成功{"=" * 5}')
    except Exception as e:
        logging.exception(e)
        logging.info(f'{"=" * 5}连接失败{"=" * 5}')


def send_all_result2pms():
    with open('pms_job.json', 'r', encoding='utf-8') as f:
        base_info = json.load(f)

    if base_info['task_id'] is 0 or base_info['product_id'] is 0:
        logging.info(f'task_id：{base_info["task_id"]},product_id：{base_info["product_id"]}')
        logging.info(f'不上传测试结果到pms')
        return

    with open('result.json', 'r', encoding='utf-8') as f:
        result_dict = json.load(f)

    logging.info(f'{"=*" * 30}开始上传所有测试结果到pms{"=*" * 30}')
    for item in result_dict:
        send_result2pms(item, result_dict[item])
    logging.info(f'{"=*" * 30}所有测试结果上传到pms完毕{"=*" * 30}')


if __name__ == '__main__':
    send_all_result2pms()
