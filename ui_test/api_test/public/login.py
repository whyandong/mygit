# coding:utf-8

import yaml
import os
from interface.requests_all import request_method


def getUserInfo():
    userfile = os.path.join(os.getcwd(),"config/userinfo.yaml")
    userinfo_file = open(userfile, "r")
    info = yaml.load(userinfo_file, Loader=yaml.FullLoader)
    userinfo_file.close()

    return info


def getToken():
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:51.0) Gecko/20100101 Firefox/51.0",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "application/json",
    }
    info = getUserInfo()
    requ = request_method()
    parms = {
        "captchaId": "",
        "userId": info['userid'],
        "userPassword": info["userpwd"],
        "vcode": ""
    }
    reponse = requ.post(url=info['loginurl'], headers=headers, params=parms)
    return reponse['data']['token']
