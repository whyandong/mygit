# -*- coding:utf-8 -*-
import os
import json

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#data/web_oauth2测试数据目录路径
center_path = os.path.join(os.path.join(root_path,'data/web_oauth2'))


linglong = os.path.join(os.path.join(root_path,'data/linglong'))

add_app = os.path.join(linglong,'add_app.json')
upload_file = os.path.join(linglong,'upload_file.json')
delete_app = os.path.join(linglong,'delete_app.json')
app_store = os.path.join(linglong,'app_store.json')
deleteapp = os.path.join(linglong,'deleteapp.json')
idupdate = os.path.join(linglong,'id_update.json')


#data/web_oauth2目录下测试数据路径
key_abspath = os.path.join(center_path,"key_1.json")
center_abspath = os.path.join(center_path,"center_1.json")
authorization_abspath = os.path.join(center_path, "authorization_1.json")

#data/Account_center 测试数据目录路径
account_center = os.path.join(os.path.join(root_path,'data/Account_center'))
ars_path = os.path.join(os.path.join(root_path,'configs'))

#data/Unionid_Client 测试数据路径
Unionid_Bind = os.path.join(os.path.join(root_path,'data/Unionid_Client/Unionid_Bind'))
ars_path = os.path.join(os.path.join(root_path,'configs'))
#生成uosid
get_uosid_path = os.path.join(Unionid_Bind,"get_uosid.json")
#本地账号与网络账号绑定
bind_unionid = os.path.join(Unionid_Bind,"bind_unionid.json")
bind_unionid_1 = os.path.join(Unionid_Bind,"bind_unionid_1.json")
bind_unionid_2 = os.path.join(Unionid_Bind,"bind_unionid_2.json")
bind_unionid_3 = os.path.join(Unionid_Bind,"bind_unionid_3.json")

#检测uosid是否有效
localbind_uosid = os.path.join(Unionid_Bind,"localbind_uosid.json")
#解绑本地
unbind_unionid = os.path.join(Unionid_Bind,"unbind_unionid.json")
unbind_unionid_1 = os.path.join(Unionid_Bind,"unbind_unionid_1.json")

#发送验证码
get_captcha = os.path.join(Unionid_Bind,"get_captcha.json")
get_captcha_1 = os.path.join(Unionid_Bind,"get_captcha_1.json")
#登入验证
valid_login = os.path.join(Unionid_Bind,"valid_login.json")
valid_login_1 = os.path. join(Unionid_Bind,"valid_login_1.json")
valid_login_2 = os.path.join(Unionid_Bind,"valid_login_2.json")
valid_login_3 = os.path.join(Unionid_Bind,"valid_login_3.json")
#用于检测本地账号与网络账号进行绑定
bindcheck = os.path.join(Unionid_Bind,"bindcheck.json")




#data/update_platform测试数据路径
update_platform = os.path.join(os.path.join(root_path,'data/update_platform'))
platform_admin = os.path.join(os.path.join(root_path,'data/platform_admin'))

#更新平台apt转发接口
apt_repository =  os.path.join(update_platform,"apt_update.json")

apt_repository_all =  os.path.join(update_platform,"apt_update_all.json")
apt_repository_1 =  os.path.join(update_platform,"apt_update_1.json")

apt_repository_2 =  os.path.join(update_platform,"apt_update_2.json")


apt_repository_3 =  os.path.join(update_platform,"apt_update_3.json")


apt_repository_4 =  os.path.join(update_platform,"apt_update_4.json")

apt_repository_5 =  os.path.join(update_platform,"apt_update_5.json")

apt_repository_6 =  os.path.join(update_platform,"apt_update_6.json")

apt_repository_7 =  os.path.join(update_platform,"apt_update_7.json")

apt_repository_8 =  os.path.join(update_platform,"apt_update_8.json")

apt_repository_9 =  os.path.join(update_platform,"apt_update_9.json")

apt_repository_test =  os.path.join(update_platform,"apt_update_test.json")

#更新平台结果上报接口
update_satus = os.path.join(update_platform,"update_status.json")

update_satus_1 = os.path.join(update_platform,"update_status_1.json")
update_satus_2 = os.path.join(update_platform,"update_status_2.json")

update_satus_3 = os.path.join(update_platform,"update_status_3.json")
update_satus_4 = os.path.join(update_platform,"update_status_4.json")
update_satus_5 = os.path.join(update_platform,"update_status_5.json")





#更新平台同步接口
license_sync = os.path.join(update_platform,"license_sync.json")
license_sync_1 = os.path.join(update_platform,"license_sync_1.json")
license_sync_2 = os.path.join(update_platform,"license_sync_2.json")

license_sync_3 = os.path.join(update_platform,"license_sync_3.json")
license_sync_4 = os.path.join(update_platform,"license_sync_4.json")
license_sync_5= os.path.join(update_platform,"license_sync_5.json")

#日志同步接口
systemupdatelogs_1 = os.path.join(update_platform,"systemupdatelogs_1.json")

systemupdatelogs_2 = os.path.join(update_platform,"systemupdatelogs_2.json")

systemupdatelogs_3 = os.path.join(update_platform,"systemupdatelogs_3.json")



#查看任务进度接口
task_progress_1 = os.path.join(platform_admin,"task_progress_1.json")
task_progress_2 = os.path.join(platform_admin,"task_progress_2.json")
task_progress_3 = os.path.join(platform_admin,"task_progress_3.json")
task_progress_4 = os.path.join(platform_admin,"task_progress_4.json")

#查看任务详情终端
task_terminal_1 = os.path.join(platform_admin,"task_terminal_1.json")
task_terminal_2 = os.path.join(platform_admin,"task_terminal_2.json")
task_terminal_3 = os.path.join(platform_admin,"task_terminal_3.json")
task_terminal_4 = os.path.join(platform_admin,"task_terminal_4.json")
task_terminal_5 = os.path.join(platform_admin,"task_terminal_5.json")

#查看任务列表
task_1 = os.path.join(platform_admin,"task_1.json")
task_2 = os.path.join(platform_admin,"task_2.json")
task_3 = os.path.join(platform_admin,"task_3.json")
task_4 = os.path.join(platform_admin,"task_4.json")


#创建任务
task_add_1 = os.path.join(platform_admin,"task_add_1.json")
task_add_2 = os.path.join(platform_admin,"task_add_2.json")
task_add_3 = os.path.join(platform_admin,"task_add_3.json")
task_add_4 = os.path.join(platform_admin,"task_add_4.json")


#创建仓库地址
task_reposourceurl_1 = os.path.join(platform_admin,"task_reposourceurl_1.json")
task_reposourceurl_2 = os.path.join(platform_admin,"task_reposourceurl_2.json")
task_reposourceurl_3 = os.path.join(platform_admin,"task_reposourceurl_3.json")






resource_root_path = os.path.join(os.path.join(root_path, 'resource'))
configs_root_path = os.path.join(os.path.join(root_path, 'configs'))
log_root_path = os.path.join(os.path.join(root_path, 'log'))
image_path = os.path.join(os.path.join(root_path, 'log', 'image'))
script_root_path = os.path.join(os.path.join(root_path, 'script'))
allure_results_path = os.path.join(root_path, 'allure-results')
allure_report_path = os.path.join(root_path, 'allure-report')
execute_file = os.path.join(root_path, 'execute.txt')
skip_list_file = os.path.join(root_path, 'skip_list.txt')



config_path = os.path.join(os.path.join(root_path,'configs/test_public'))

unionTest_config_file = os.path.join(root_path, 'UnionTestConfig.json')


with open(unionTest_config_file, 'r', encoding='utf-8') as j:
    unionTest_config = json.load(j)

if not os.path.exists(image_path):
    os.makedirs(image_path)

write_result_log_dir = None  # 将结果记录到本地
write_result_temp_dir = log_root_path  # 与测试客户端通过文件交互
