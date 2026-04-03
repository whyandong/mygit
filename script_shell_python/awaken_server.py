#!/usr/bin/python3
# -*- coding: UTF-8 -*-


import flask
import json
from gevent import pywsgi
from wakeonlan import wake
import os

#__name__代表当前的python文件。把当前的python文件当做一个服务启动
server=flask.Flask(__name__)


#第一个参数就是路径,第二个参数支持的请求方式，不写的话默认是get
@server.route('/wakeUpInterface',methods=['post'])
def test_results():
    # 接收数据
    ret = flask.request.get_json()
    msg = ret.get("msg")
    
    os.system("sleep 45  && wakeonlan 1c:83:41:70:92:0f") 


    res={'msg_code':200,'data':{"commit_id":""},'msg':'接收数据成功'}

    return json.dumps(res,ensure_ascii=False)

if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0',9527),server)
    server.serve_forever()