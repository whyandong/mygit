
# -*- coding:utf8 -*
from frame.get_public import account_encrypt
from frame.anasyls import get_state
import allure
import requests
from frame.projectLog import log
import os
from frame.constant import center_path
from frame.read_config import get_values_from_config

from frame.read_json import get_read_json
from frame.read_json import post_read_json
from frame.constant import key_abspath,center_abspath,authorization_abspath
import re
logger=log()



@allure.step("第一步 用户中心获取state")
def center_key():
    data_1=get_read_json(center_abspath)
    url = data_1[0][1]
    headers = data_1[0][2]
    result = requests.get(url=url, headers=headers)
    result_code = result.status_code
    url = result.url

    return url



@allure.step("第二步 获取秘钥")
def oauth_key():
    data_2=get_read_json(key_abspath)
    url = data_2[0][1]
    headers = data_2[0][2]
    result=requests.get(url=url,headers=headers)
    result_code=result.status_code
    result_data=result.json()['data']

    return result_data

@allure.step("第三步 登录验证及授权")
def authorization_key():
    data_3=post_read_json(authorization_abspath)
    datas=data_3[0][3]
    datas['state']=get_state('state',center_key())
    datas['password']=account_encrypt(get_values_from_config("password","user_info"),oauth_key())
    datas['account']=account_encrypt(get_values_from_config("account","user_info"),oauth_key())

    url=data_3[0][1]
    headers=data_3[0][2]
    result=requests.post(url=url,data=datas,headers=headers)
    result_date=result.json()
    result_code=result_date['code']
    response=result.headers['Set-Cookie']
    uniontech_cookie=re.search('(uniontech=.*?); ',response).group(1)[10:]


    return uniontech_cookie



if __name__ == '__main__':

    ps=authorization_key()










