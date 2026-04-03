# -*- coding: utf-8 -*-
"""
@Time ： 2021/6/21 下午4:26
@Auth ： zhanyuanyuan
@File ：get_method.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
import requests

def get_method(url,headers):
    try:
       result=requests.get(url=url,headers=headers)
       result_code=result.status_code
       result_dict = result.json()
       return result,result_code,result_dict
    except Exception as false:
        print(false)

def post_method(url,headers,request):

    try:
       result = requests.post(url=url,headers=headers,data=request)
       result_code = result.status_code
       result_dict = result.json()
       return result, result_code,result_dict

    except Exception as false:
        print(false)