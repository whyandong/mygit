# -*- coding: utf-8 -*-

from interface.requests_all import request_method
from public import login
import fake_useragent

reques = request_method()


class Api(object):

    def __init__(self, url, parms, method):
        self.url = url
        self.headers = {
            'User-Agent': fake_useragent.UserAgent().random,
            'Content-Type': 'application/json'
        }
        self.parms = parms
        self.method = method
        # self.headers.setdefault('Authorization', login.getToken())

    def testapi(self):
        if self.method == 'POST':
            self.response = reques.post(url=self.url,
                                        headers=self.headers,
                                        params=self.parms)
        elif self.method == "GET":
            self.response = reques.get(url=self.url,
                                       headers=self.headers,
                                       params=self.parem)
        return self.response

    def getJson(self):
        json_data = self.testapi()
        return json_data
