# -*- coding:utf-8 -*-
import os
import json

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
resource_root_path = os.path.join(os.path.join(root_path, 'resource'))
configs_root_path = os.path.join(os.path.join(root_path, 'configs'))
data_config_path = os.path.join(configs_root_path, 'data_config.xml')
data_config_development_path = os.path.join(configs_root_path,
                                            'data_config_develop.xml')

if os.path.exists(data_config_development_path):
    data_config_path = data_config_development_path

log_root_path = os.path.join(os.path.join(root_path, 'log'))
image_path = os.path.join(os.path.join(root_path, 'log', 'image'))
script_root_path = os.path.join(os.path.join(root_path, 'script'))

allure_results_path = os.path.join(root_path, 'allure-results')
allure_report_path = os.path.join(root_path, 'allure-report')

report_path = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

skip_list_file = os.path.join(root_path, 'skip_list.txt')

allure_path = '/usr/bin/allure/bin/'

unionTest_config_file = os.path.join(root_path, 'UnionTestConfig.json')
with open(unionTest_config_file, 'r', encoding='utf-8') as j:
    unionTest_config = json.load(j)
# ut002037 modify
if unionTest_config['modules']['ci-case-health'] != '':
    execute_file = os.path.join(root_path, unionTest_config['modules']['ci-case-health'])
else:
    execute_file = os.path.join(root_path, 'execute.txt')


if not os.path.exists(image_path):
    os.makedirs(image_path)

write_result_log_dir = None  # 将结果记录到本地
write_result_temp_dir = log_root_path  # 与测试客户端通过文件交互

resoure_path = resource_root_path
dbus_path = os.path.join(os.path.join(resoure_path, 'dbus'))
deb_path = os.path.join(os.path.join(resoure_path, 'deb'))

if not os.path.exists(dbus_path):
    os.mkdir(dbus_path)
