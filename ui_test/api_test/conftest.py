# -*- coding: utf-8 -*-
"""
定制html页面报告展示内容
"""
import pytest
from py._xmlgen import html
import yaml
import os
from time import strftime
from interface.oper_excel import writeCaseResult
import sys

configfile = os.path.join(os.getcwd(), 'config/config.yaml')
config_file = open(configfile, "r", encoding='utf-8')
configs = yaml.load(config_file, Loader=yaml.FullLoader)
config_file.close()


def pytest_collection_modifyitems(items):
    # item表示每个测试用例，解决用例名称中文显示问题
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode-escape")
        item._nodeid = item._nodeid.encode("utf-8").decode("unicode-escape")


@pytest.mark.optionalhook
def pytest_html_report_title(report):
    report.title = configs['title']


def pytest_configure(config):
    config._metadata.clear()
    config._metadata['测试人'] = configs['tester']
    config._metadata['测试地址'] = configs['testaddr']
    config._metadata['测试版本'] = configs['version']


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('用例描述', class_="sortable",
                            col="name"))  # 表头添加Description
    cells.insert(4, html.th('执行时间', class_='sortable time', col='time'))
    cells.pop(-1)


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.description, class_="col-description"))
    cells.insert(4, html.td(strftime('%Y-%m-%d %H:%M:%S'), class_='col-time'))
    cells.pop(-1)


@pytest.mark.hookwrapper
# @pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if item.function.__doc__ is None:
        report.description = str(item.function.__name__)
    else:
        report.description = str(item.function.__doc__)
    if report.when == 'call':
        writeCaseResult(sys.argv[1], report.description, report.outcome)
    report.nodeid = report.nodeid.encode("utf-8").decode("unicode_escape")
