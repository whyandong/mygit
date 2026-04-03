#!/usr/bin/python3 

import pandas as pd

item_list = ["power_off_start_time","power_off_end_time","power_On_start_time","power_On_end_time","reboot_start_time",
    "reboot_end_time","standby_start_time","standby_lower_time","standby_waken_start_time","standby_waken_end_time","dormancy_start_time","dormancy_end_time"]




time_dict = {}

# 读取文件获取测试时间
with open ("/home/uos/logs/timeRecordSheet.log" ,'r',encoding='utf8')as fp:
    read_item = fp.readlines()
    count = len(read_item)


    for a in range(count):
        if read_item[a].replace("\n","").split(" ")[0] in item_list:
            time_dict[read_item[a].replace("\n","").split(" ")[0]] = read_item[a].replace("\n","").split(" ")[1:]


# 数据计算方法
def calculation(end_count,start_count):
    ret = (pd.to_datetime(time_dict[item_list[end_count]][-1].split("_")[-1]) - pd.to_datetime(time_dict[item_list[start_count]][-1].split("_")[-1])).total_seconds()
    return ret



result_dict={
    "shutdown":calculation(1,0),
    "open": calculation(3,2),
    "reboot":calculation(5,4),
    "S3":calculation(7,6),
    "S3_wake_up":calculation(9,8),
    "S4":calculation(11,10)
}

print(result_dict)