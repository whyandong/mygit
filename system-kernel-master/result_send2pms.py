# -*- coding: utf-8 -*-
import os
import json
import logging
from urllib import request, parse

from frame import constant

result_dict = {}
info_dict_template = {
    'steps': {
        'setup': {
            'result': False,
            'longrepr': None
        },
        'call': {
            'result': False,
            'longrepr': None
        },
        'teardown': {
            'result': False,
            'longrepr': None
        }
    },
    'result': '',
    'longrepr': ''
}


def send_result2pms(script_path, info_dict):
    if constant.unionTest_config['transform']['style'] == 'full':
        # 针对结果文件的key字段进行处理 ut002037 2021.7.30
        script = script_path.split("::")[1]
    elif constant.unionTest_config['transform']['style'] == 'simple':
        script = os.path.split(script_path)[1].split('.')[0]
    else:
        msg = r'请将transform.style配置为 full、simple中的一种'
        logging.exception(msg)
        raise RuntimeError(msg)

    with open(os.path.join(constant.root_path, 'resource', 'pms',
                           'pms_job.json'),
              'r',
              encoding='utf-8') as f, open(os.path.join(
                  constant.root_path, 'resource', 'pms', 'name2id.json'),
                                           'r',
                                           encoding='utf-8') as f2:
        base_info = json.load(f)
        pms_case_id = json.load(f2).get(script, "")

    if not pms_case_id:
        logging.info(
            f'{"=" * 5}未查到用例{script_path}对应的pms编号,请及时刷新resource/pms/name2id.json文件内容{"=" * 5}'
        )
        return

    if base_info['task_id'] == 0 or base_info['product_id'] == 0:
        logging.info(
            f'task_id:{base_info["task_id"]},product_id:{base_info["product_id"]}'
        )
        logging.info(f'不上传测试结果到pms')
        return

    logging.info(f'script_path:{script_path}')
    logging.info(f'info_dict:{info_dict}')

    post_data = {
        'product_id': base_info['product_id'],
        'task_id': base_info['task_id'],
        'case_id': pms_case_id,
        'result': info_dict['result'],
        'reals': info_dict['longrepr'],
    }

    if base_info.get('suite_name', None):
        post_data['suite_name'] = base_info['suite_name']

    if base_info.get('test_type', None):
        post_data['test_type'] = base_info['test_type']

    if base_info.get('user_name', None):
        post_data['user_name'] = base_info['user_name']

    if base_info.get('area', None):
        post_data['area'] = base_info['area']

    if base_info.get('testtask_name', None):
        post_data['testtask_name'] = base_info['testtask_name']

    logging.info(f'上传{pms_case_id}测试结果到pms')
    logging.info(f'post_data:{post_data}')
    try:
        response = request.urlopen(
            base_info['baseurl'],
            data=parse.urlencode(post_data).encode('utf-8'))
        logging.info(f'response:{response.read().decode()}')
        logging.info(f'{"=" * 5}连接成功{"=" * 5}')
    except Exception as e:
        logging.exception(e)
        logging.info(f'{"=" * 5}连接失败{"=" * 5}')


def send_all_result2pms():
    with open(os.path.join(constant.root_path, 'resource', 'pms',
                           'pms_job.json'),
              'r',
              encoding='utf-8') as f:
        base_info = json.load(f)

    if base_info['task_id'] == 0 or base_info['product_id'] == 0:
        logging.info(
            f'task_id:{base_info["task_id"]},product_id:{base_info["product_id"]}'
        )
        logging.info(r'不上传测试结果到pms')
        return

    logging.info(f'{"=*" * 30}开始上传所有测试结果到pms{"=*" * 30}')
    for item in result_dict:
        send_result2pms(item, result_dict[item])
    logging.info(f'{"=*" * 30}所有测试结果上传到pms完毕{"=*" * 30}')


def set_path(log_dir=None, tmp_dir=None):
    constant.write_result_log_dir = log_dir
    constant.write_result_temp_dir = tmp_dir


def write_result2file():
    file_name = 'result.json'
    if constant.write_result_log_dir is not None:
        file_path = os.path.join(constant.write_result_log_dir, file_name)
        with open(file_path, 'w', encoding='utf8') as f:
            json.dump(result_dict, f, ensure_ascii=False)

    if constant.write_result_temp_dir is not None:
        file_path = os.path.join(constant.write_result_temp_dir, file_name)
        simple_result_dict = {
            key: {
                "result": result_dict[key]["result"],
                "longrepr": result_dict[key]["longrepr"]
            }
            for key in result_dict
        }
        with open(file_path, 'w', encoding='utf8') as f:
            json.dump(simple_result_dict, f, ensure_ascii=False)


def write_total_run_script2file(items):
    file_name = 'total.json'
    detailed_run_case_file = 'detailed_run_case.txt'
    if constant.write_result_temp_dir is not None:
        file_path = os.path.join(constant.write_result_temp_dir, file_name)
        detailed_run_case_file_path = os.path.join(
            constant.write_result_temp_dir, detailed_run_case_file)
        total_result = {"total": len(items)}
        with open(file_path, 'w', encoding='utf8') as f:
            json.dump(total_result, f, ensure_ascii=False)

        with open(detailed_run_case_file_path, 'w', encoding='utf8') as f:
            if len(items) == 1:
                f.write(f'{items[0].nodeid}')
                return

            if len(items) > 1:
                for item in items[:-1]:
                    f.write(f'{item.nodeid}\r')

                f.write(f'{items[-1:][0].nodeid}')
