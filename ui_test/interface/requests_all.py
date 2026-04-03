# -*- coding: utf-8 -*-
import json
import requests
import urllib3
from public.log import LOG, logger

urllib3.disable_warnings()


@logger('requests封装')
class request_method():

    def __init__(self):
        pass

    def get(self, url, headers):
        """
        get请求
        """
        try:
            reponse = requests.get(url, headers=headers, verify=False)
            reponse.encoding = 'UTF-8'
            json_response = json.loads(reponse.text)
            return json_response
        except Exception as e:
            LOG.error('get请求出错,出错原因:%s' % e)
            return {}

    def post(self, url, headers, params):
        """
        post请求
        """
        try:
            if 'open' in params:
                files = eval(params)
                reponse = requests.post(url=url,
                                        files=files,
                                        headers=headers,
                                        verify=False)
            else:
                if isinstance(params, str) and params.startswith('['):
                    data = params
                elif isinstance(params, str) and params.startswith('{'):
                    params = eval(params)
                    data = json.dumps(params)
                else:
                    data = json.dumps(params)
                
                reponse = requests.post(url=url,
                                        data=data,
                                        headers=headers,
                                        verify=False)
            json_response = json.loads(reponse.text)
            return json_response
        except Exception as e:
            LOG.error('post请求出错,出错原因:%s' % e)
            return {}

    def delete(self, url, headers, params):
        """
        delete请求
        """
        try:
            reponse = requests.delete(url=url,
                                      params=params,
                                      headers=headers,
                                      verify=False)
            json_response = json.loads(reponse.text)
            return json_response
        except Exception as e:
            LOG.error('delete请求请求出错,出错原因:%s' % e)
            return {}

    def put(self, url, headers, params):
        """
        put请求
        """
        try:
            data = json.dumps(params)
            reponse = requests.put(url=url,
                                   headers=headers,
                                   data=data,
                                   verify=False)
            json_response = json.loads(reponse.text)
            return json_response
        except Exception as e:
            LOG.error('put请求出错,出错原因:%s' % e)
            return {}
