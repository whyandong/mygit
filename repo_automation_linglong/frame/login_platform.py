
import requests

s = requests.Session()
class Login_Platform:

    def login_platform(self):
           url = "http://gray-update-admin-pre.uniontech.com/api/v1/oauth/login"
           login_url = s.get(url=url).url
           data = {
                "username": "zhanghongwei",
                "password": "admin888",
                "captcha": ""
            }

           result = s.post(url=login_url, data=data, verify=False)