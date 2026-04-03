# -*- coding:utf-8 -*-
import pytest

from frame import constant
from frame import uparser
from frame.uparser import pytest_args
from frame.get_case import get_case
from frame.allure_report import save_report_history
import os
from result_send2pms import send_all_result2pms

if __name__ == '__main__':
    save_report_history()
    if not uparser.args.id:
        case_list = get_case()
        [pytest_args.append(item) for item in case_list]

    pytest.main(pytest_args)
    os.system(f"/usr/bin/allure/bin/allure generate {constant.allure_results_path} -o {constant.allure_report_path} --clean")
    if constant.unionTest_config['transform']['mode'] == 'delay':  # 延迟上传，即测试完后上传
        send_all_result2pms()
