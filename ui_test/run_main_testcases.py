# -*- coding: utf-8 -*-
"""
自动化测试入口
"""
import os
import pytest
from datetime import datetime
from public.send_email import sendemail
import sys

sys.path.append(os.getcwd())


def useage():
    print(
        "windows: python run_main_testcases.py system/web(system或web用例标识)  skip(跳过用例)/test(执行所有用例)" +
        "\nLinux: python3 run_main_testcases.py system/web(system或web用例标识) skip(跳过用例)/test(执行所有用例)"
    )


def run_test_cases():
    reportname = '自动化测试报告%s.html' % datetime.now().strftime("%Y-%m-%d-%H-%M")
    file_dir = os.path.join(os.getcwd(), 'report')
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    
    reportfile = os.path.join(file_dir, reportname)
    casedir = os.path.join(os.getcwd(), 'testcases')
    casefilepath = os.path.join(os.getcwd(), 'casefile', 'case.xls')
    with open(reportfile, 'w+') as f:
        pass
    casemark = sys.argv[1]
    pytest.main([
        '-W ignore::DeprecationWarning', '-m ' + casemark, casedir,
        '--html=' + reportfile, '--self-contained-html'
    ])
    sendemail(reportfile, reportname, casefilepath, 'case.xls')


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        useage()
    else:
        run_test_cases()
