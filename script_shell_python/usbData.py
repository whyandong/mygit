#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os


def cmd(cmd):
    '''
    调用shell命令返回执行结果
    '''
    r = os.popen(cmd).read()
    log = r.split("\n")
    lists = [x for x in log if x!=''] 
    return lists

def avg_list(rw_lsit):
    leng = len(rw_lsit)
    list_sum = 0
    for a in range(len(rw_lsit)):
        list_sum = list_sum + rw_lsit[a]
    
    avg_list = list_sum/leng
    # print(list_sum/leng)
    return avg_list

def read_usb(path):
    list_data = cmd("awk '/copied/{print $(NF-1)}' %s/usb.log" %path)
    # print (list_data)
    list_un = []
    for aa in list_data:
        list_un.append(float(aa))

    if len(list_un) == 12 :
        write = list_un[::2]
        # print(write)
        
        read = list_un[1::2]
        # print(read)

        if len(write) == 6 and len(read) == 6:
            usb_dict =["%.3f" %avg_list(write[0:3]),"%.3f" %avg_list(read[0:3]),"%.3f" %avg_list(write[3:]),"%.3f" %avg_list(read[3:])]
        print (usb_dict)
    
        return usb_dict
    else:
        exit()



if __name__ == '__main__':
    # pathfile = os.path.abspath(__file__)
    # print (pathfile)

    path = "/home/uos/"
    if os.path.exists("%susb.log" %path):
        avg_list = read_usb(path)

        # 写入结果到文件
        with open("%s/usb.log" %(path),"a+") as f:
            for a in avg_list:
                # print(a)
                f.write("%s\n" %a)
