# -*- coding:utf-8 -*-
# -*- coding: utf-8 -*-
import os
import logging
import pytest
from frame import constant
from frame import uparser
from frame.uparser import pytest_args
from frame.get_case import get_case
from frame.allure_report import save_report_history
from result_send2pms import send_all_result2pms
# 20210730 ut002037 引入该函数避免手动完成name2id的转换
from tojson import get_step

if __name__ == '__main__':
    save_report_history()

    if not uparser.args.id:
        module = uparser.args.module
        module_execute_dict = constant.unionTest_config['modules']
        if module:
            execute_module_file_path = module_execute_dict.get(
                uparser.args.module, None)
            if execute_module_file_path:
                logging.info(f'当前执行module为:{module}')
                constant.execute_file = os.path.join(constant.root_path,
                                                     execute_module_file_path)
            else:
                logging.info(f'未找到module: {module}相关信息')
                raise RuntimeError(f'未找到module: {module}相关信息')

        case_list = get_case()
        print(len(case_list))
        [pytest_args.append(item) for item in case_list]

    # 扫描constant.execute_file文件，获取执行用例id与用例名称对应关系，实现结果回填
    get_step()
    pytest.main(pytest_args)

    os.system(
        f"allure generate --clean {constant.allure_results_path} -o {constant.allure_report_path}"
    )
    if constant.unionTest_config['transform'][
            'mode'] == 'delay':  # 延迟上传，即测试完后上传
        send_all_result2pms()
