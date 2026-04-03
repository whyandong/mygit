# -*- coding: utf-8 -*-
import os
from frame import constant, common


def save_report_history():
    """
    处理history文件，allure生成趋势报告
    :return:None
    """
    history_path = os.path.join(constant.allure_report_path, 'history')

    if os.path.exists(constant.allure_results_path):
        os.system(f'rm -r {constant.allure_results_path}')
        os.makedirs(constant.allure_results_path)

    if os.path.exists(history_path):
        common.execute_command(f'cp -r {history_path} {constant.allure_results_path}')
