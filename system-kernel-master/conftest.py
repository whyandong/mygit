# -*- coding:utf-8 -*-
import sys
import copy
import logging

import pytest

from frame import constant
from frame import get_case
from result_send2pms import result_dict, info_dict_template, write_result2file, send_result2pms, \
    write_total_run_script2file

sys.path.append(constant.root_path)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # 获取钩子方法的调用结果
    out = yield

    # 3. 从钩子方法的调用结果中获取测试报告
    report = out.get_result()

    logging.info(f"{report.nodeid}:{report.when}")

    if constant.unionTest_config is not None:
        if constant.unionTest_config.get('transform', None):
            if constant.unionTest_config['transform'].get('style') == 'full':
                script_path = report.nodeid
            elif constant.unionTest_config['transform'].get(
                    'style') == 'simple':
                script_path = report.nodeid.split('::')[0]
            else:
                script_path = report.nodeid.split('::')[0]
        else:
            script_path = report.nodeid.split('::')[0]
    else:
        script_path = report.nodeid.split('::')[0]

    if script_path in result_dict:
        info_dict = result_dict[script_path]
    else:
        info_dict = copy.deepcopy(info_dict_template)
        result_dict[script_path] = info_dict

    # report相关信息参见 _pytest/reports.py::TestReport 源码
    info_dict['steps'][report.when]['result'] = report.outcome
    info_dict['steps'][report.when]['longrepr'] = str(report.longrepr)

    # call相关信息参见 _pytest/runner.py::CallInfo 源码
    # call.excinfo 为ExceptionInfo对象,相关信息参见 _pytest/_code/code.py::ExceptionInfo 源码
    # str(report.longrepr) 可以获取堆栈信息
    if call.excinfo:
        if AssertionError.__name__ == call.excinfo.typename:
            info_dict['result'] = 'fail'
            info_dict['longrepr'] = '测试不通过'
        else:
            info_dict['result'] = 'blocked'
            info_dict['longrepr'] = '测试发生错误'

    if report.when == 'teardown':
        if not info_dict['result']:
            info_dict['result'] = 'pass'
            info_dict['longrepr'] = '测试通过'

        write_result2file()
        if constant.unionTest_config['transform'][
                'mode'] == 'immediately':  # 立即上传
            send_result2pms(script_path, result_dict[script_path])


@pytest.hookimpl(hookwrapper=True)
def pytest_collection_modifyitems(config, items):
    yield

    item_info_template = {'item': '', 'nodeid': '', 'file': ''}

    delete_case = get_case.get_skip_list()
    logging.info(f'delete_case: {delete_case}')
    delete_module = []
    delete_file = []
    delete_function = []

    delete_list = []

    items_info_list = []

    for item in items:
        item_info = copy.deepcopy(item_info_template)
        item_info['item'] = item
        item_info['nodeid'] = item.nodeid
        item_info['file'] = item.nodeid.split('::')[0]
        items_info_list.append(item_info)

    for item in delete_case:
        if '::' in item:
            delete_function.append(item)
        elif item[-3:] == '.py':
            delete_file.append(item)
        else:
            delete_module.append(item)

    [
        delete_list.append(item['item']) for module in delete_module
        for item in items_info_list if item['file'].startswith(f'{module}/')
    ]

    [
        delete_list.append(item['item']) for file in delete_file
        for item in items_info_list
        if item['file'] == file and item['item'] not in delete_list
    ]

    [
        delete_list.append(item['item']) for function in delete_function
        for item in items_info_list
        if item['nodeid'] == function and item['item'] not in delete_list
    ]

    for case in delete_list:
        items.remove(case)

    write_total_run_script2file(items)
