#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flask
import json
from gevent import pywsgi
import threading
import os

#__name__代表当前的python文件。把当前的python文件当做一个服务启动
server=flask.Flask(__name__)


#第一个参数就是路径,第二个参数支持的请求方式，不写的话默认是get
@server.route('/wake',methods=['post'])
def test_results():
    # 接收数据
    ret = flask.request.get_json()

    # 获取请求传入的commit id
    request_ip = ret.get("IP")

    def wakeUp(ip):
        os.system("wakeonlan %s" %ip)
        print ("发送请求唤醒的测试设备：IP【%s】" %ip)

    start = threading.Timer(50,wakeUp,(request_ip,))

    start.start()

    res={'msg_code':200,'data':{"IP":request_ip},'msg':'接收数据成功'}
    print (res)


    return json.dumps(res,ensure_ascii=False)
    


if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0',6666),server)
    server.serve_forever()