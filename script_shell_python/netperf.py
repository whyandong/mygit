#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sys
import numpy as np

def cmd(cmd):
    '''
    调用shell命令返回执行结果
    '''
    r = os.popen(cmd).read()
    log = r.split("\n")
    lists = [x for x in log if x!=''] 
    return lists

#检索文件名
def readname(path):
    filelist = os.listdir(path)
    filename = ""

    # print(filelist)
    for a in filelist:
        if "netperf" in a:
            filename = a
    if filename == "":
        return 1
    else:
        return filename

#转换数字型字符--->float
def type_list(net_list):
    new = []
    for a in net_list:
        new.append(float(a))
    return new

#数据处理主函数
def read_netprtf(path,filename):

    #未检索到文件名，函数返回
    if filename == 1:
        print("不存在netprtf测试数据，程序退出")
        return

    tcp_stream = cmd("cat %s/%s |grep -A 7  \"TCP STREAM\" |awk '/^[0-9]/{print $NF}'" %(path,filename))
    # print(tcp_stream)

    tcp_rr = cmd("cat %s/%s |grep -A 7  \"TCP REQUEST\" |awk '/^[0-9]/{print $0}'|awk 'NF>2{print $NF}' " %(path,filename))
    # print(tcp_rr)

    tcp_crr = cmd("cat %s/%s |grep -A 6  \"TCP Connect\" |awk '/^[0-9]/{print $NF}'" %(path,filename))
    # print (tcp_crr)

    udp_stream = cmd("cat %s/%s |grep -A 6  \"UDP STREAM\" |awk '/^[0-9]/{print $NF}'" %(path,filename))
    # print (tcp_stream)

    udp_crr = cmd("cat %s/%s | grep -A 7  \"UDP REQUEST\" |awk '/^[0-9]/{print $0}'|awk 'NF>2{print $NF}'" %(path,filename))
    # print (udp_crr)


    if len(tcp_stream) == len(tcp_rr) == len(tcp_crr) == len(tcp_stream) ==  len(udp_crr):
        print("netprtf测试数据正常")
    else:
        print("netprtf测试数据存在错误,可能有部分测试项未获取到数据")

        # return

    #转换数据类型，计算平均数
    netperf_dict = {
        "tcp_stream":np.mean(type_list(tcp_stream)),
        "tcp_rr":np.mean(type_list(tcp_rr)),
        "tcp_crr":np.mean(type_list(tcp_crr)),
        "udp_stream":np.mean(type_list(udp_stream)),
        "udp_crr":np.mean(type_list(udp_crr)),
    }

    # print(netperf_dict)
    return netperf_dict

if __name__ == '__main__':

    if len(sys.argv) == 2:
        print("="*100)
        path = sys.argv[1]

        #定义结果文件名
        netperf_result = "netperf_result.txt"

        #测试数据目录
        # path = "/home/uos/logs"
        if os.path.exists("%s/%s" %(path,netperf_result)):
            print("="*10)
            os.remove("%s/%s" %(path,netperf_result))

        #调用主函数获取结果
        filename = readname(path)
        result = []
        netperf_dict = read_netprtf(path,filename)
        for aa in netperf_dict:
            abc = netperf_dict[aa]
            result.append("%s : %s\n" %(aa,abc))

        #写入结果到文件
        with open("%s/%s" %(path,netperf_result),"a+") as f:
            for a in result:
                # print(a)
                f.write(a)
    else:
        print("参数错误")