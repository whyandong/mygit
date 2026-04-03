# -*- coding: utf-8 -*-
import os
import sys
import json
import logging
import argparse

from frame import constant
from frame import get_case
from frame.ulogger import UnionTestLogger

ulog = UnionTestLogger()
constant.write_result_log_dir = ulog.log_file_dir
constant.write_result_temp_dir = ulog.log_root_path

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mark', dest='mark', nargs='*', default=[])
parser.add_argument('-I', '--ID', dest='id', type=str, nargs='*', default=[])
parser.add_argument('-S', '--source', dest='source', type=str, nargs='?', default=None)
args = parser.parse_args()

pytest_args = ["-sq", "--alluredir", constant.allure_results_path]

if args.id:
    case_file_list = get_case.get_case_file_list()
    simple2full_path = {}
    args.mark = []  # 与mark互斥
    id2name_info = []
    case_list = []

    if args.source is None:
        msg = "未指定测试用例ID的来源"
        logging.exception(msg)
        raise RuntimeError(msg)
    else:
        logging.info(f'args.id: {args.id}')
        source_info = constant.unionTest_config['transform'].get(args.source, None)
        logging.info(f'id数据源为{args.source}')
        if source_info is None:
            msg = f'{constant.unionTest_config_file}文件"transform"中无{args.source}相关配置'
            logging.exception(msg)
            raise RuntimeError(msg)
        else:
            id2name_path = source_info['id2name_path']
            logging.info(f'id2name_path: {id2name_path}')
            with open(id2name_path, 'r', encoding='utf-8') as j:
                id2name_info = json.load(j)

        logging.info(f"transform.style: {constant.unionTest_config['transform']['style']}")
        if constant.unionTest_config['transform']['style'] == 'simple':
            for key_id in id2name_info:
                for case_file in case_file_list:
                    if f'{id2name_info[key_id]}.py' == os.path.split(case_file)[1]:
                        simple2full_path[id2name_info[key_id]] = case_file
                        logging.info(f'simple2full_path: {simple2full_path}')

    for item in args.id:
        if constant.unionTest_config['transform']['style'] == 'full':
            case = id2name_info.get(item, None)
            logging.info(f'case: {case}')
        elif constant.unionTest_config['transform']['style'] == 'simple':
            case_simple = id2name_info.get(item, None)
            logging.info(f'case_simple: {case_simple}')
            case = simple2full_path.get(case_simple, None)
            logging.info(f'case: {case}')
        else:
            msg = f'请将transform.style配置为 full、simple中的一种'
            logging.exception(msg)
            raise RuntimeError(msg)

        if case:
            case_list.append(case)

    if case_list:
        pytest_args.extend(case_list)
    else:
        logging.info(f'没有发现对应ID的测试脚本')
        sys.exit(0)

if args.mark:
    pytest_args = ["-m", " ".join(args.mark), "-sq", "--alluredir", constant.allure_results_path]
