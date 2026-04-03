# -*- coding:utf-8 -*-
import time
import json
import datetime
import logging

import dbus

from aw.dbus.dbus_common import get_session_dbus_interface
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.daemon.Calendar'
DBUS_PATH = '/com/deepin/daemon/Calendar/Scheduler'
IFACE_NAME = 'com.deepin.daemon.Calendar.Scheduler'


def dbus_interface():
    return get_session_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


def get_properties_value(properties: str):
    property_obj = get_session_dbus_interface(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(IFACE_NAME, properties)
    return result


def create_job(type_=1, title='job_test', rule='') -> int:
    """
    创建一个当日的日程
    :param type_:类型
    :param title:名称
    :param rule:重复规则,每日("FREQ=DAILY")，工作日("FREQ=DAILY;BYDAY=MO,TU,WE,TH,FR"),
    每周("FREQ=WEEKLY")，每月("FREQ=MONTHLY")，每年("FREQ=YEARLY")
    :return: int
    """
    job_info_dict = {"Type": type_, "Title": title, "Description": "", "AllDay": True,
                     "Start": f"{datetime.date.today().strftime('%Y-%m-%d')}T00:00:00+08:00",
                     "End": f"{datetime.date.today().strftime('%Y-%m-%d')}T23:59:00+08:00", "RRule": rule,
                     "Remind": "1;09:00", "RecurID": 0,
                     "Ignore": []}

    job_info = json.dumps(job_info_dict)
    interface = dbus_interface()
    job_id = interface.CreateJob(job_info)
    logging.info(f"创建job成功,id为{job_id}")
    return int(job_id)


def get_job_info_by_id(job_id):
    """
    通过id获取job信息
    :param job_id: job id
    :return: json
    """
    logging.info(f'获取id为{job_id}的信息')
    interface = dbus_interface()
    job_json = interface.GetJob(dbus.Int64(job_id))
    logging.info(f'job_json：{job_json}')
    return job_json


def get_job_title_by_id(job_id):
    """
    通过id获取title
    :param job_id: job id
    :return: str
    """
    job_json = get_job_info_by_id(job_id)
    job_info_dict = json.loads(job_json)
    return job_info_dict['Title']


def get_job_id(year=None, month=None, day=None) -> list:
    """
    获取某年某月某日的所有日程的id，除法定节日
    :param year: 年
    :param month: 月
    :param day: 日
    :return: list
    """

    if year is None:
        year = datetime.date.today().year
    if month is None:
        month = datetime.date.today().month
    if day is None:
        day = datetime.date.today().day

    interface = dbus_interface()
    result = interface.GetJobs(dbus.Int32(year), dbus.Int32(month), dbus.Int32(day),
                               dbus.Int32(year), dbus.Int32(month), dbus.Int32(day))

    result_list = json.loads(result)
    job_id_list = []
    for item in result_list:
        jobs = item['Jobs']
        if jobs:  # 判断是否有job
            for job in jobs:
                job_id = job["ID"]
                if job_id < 1000000:  # 排除节假日
                    job_id_list.append(job_id)

    return job_id_list


def delete_job(job_id):
    """
    根据id删除一个日程
    :param job_id:
    :return: None
    """
    logging.info(f"删除id为{job_id}的job")
    interface = dbus_interface()
    interface.DeleteJob(dbus.Int64(job_id))


def clear_all_job(job_id_list):
    """
    清理列表中所有日程
    :param job_id_list:
    :return: None
    """
    for job_id in job_id_list:
        delete_job(job_id)


def create_type():
    """
    创建一个日程类型
    :return: int
    """
    type_dict = {"Name": "测试", "Color": "#FFF000"}
    type_info = json.dumps(type_dict)
    logging.info(f"创建type,type_info:{type_info}")
    interface = dbus_interface()
    type_id = interface.CreateType(type_info)
    return type_id


@checkword
def getJobs():
    """
    GetJobs(startYear int32, startMonth int32, startDay int32,
    endYear int32, endMonth int32, endDay int32) -> (string)
    指定开始日期和结束日期。
    返回 JSON 格式
    [
     {
        "Date": "2019-01-01",
        "Jobs": [ job1, job2, ... ],
     }, ...
    ]
    @return: True or False
    """
    year = datetime.date.today().year
    interface = dbus_interface()
    result = interface.GetJobs(dbus.Int32(year), dbus.Int32(1), dbus.Int32(1),
                               dbus.Int32(year), dbus.Int32(12), dbus.Int32(31))
    if isinstance(result, dbus.String):
        try:
            json_result = json.loads(result)
            for item in json_result:
                logging.info(item)
            else:
                return True
        except json.JSONDecodeError:
            logging.info(f'返回数据不是json:{type(result)}')
            return False
    else:
        logging.info(f'返回数据类型不匹配:{type(result)}')
        return False


@checkword
def queryJobs(key="国庆"):
    """
    QueryJobs(params string) -> (string)
    params 为 JSON 格式：
    {
      "Key": "关键字",
      "Start": "2019-09-27T17:00:00+08:00",
      "End": "2019-09-27T18:00:00+08:00"
    }
    params 各字段用途：
    Key 是关键字，用于看 Job 的 Title 字段值中是否有此字符串，会忽略两头的空白，如果为空，表示不使用关键字过滤条件。
    Start 是查询时间段的开始时间，格式为 RFC3339，比如"2006-01-02T15:04:05+07:00"。
    End 是查询时间段的结束时间，格式为 RFC3339，比如"2006-01-02T15:04:05+07:00"。
    返回数据格式同 GetJobs。
    :return: True or False
    """
    year = datetime.date.today().year
    params_dict = {"Key": key, "Start": f"{year}-01-01T17:00:00+08:00", "End": f"{year}-12-31T18:00:00+08:00"}
    params = json.dumps(params_dict)
    interface = dbus_interface()
    result = interface.QueryJobs(params)
    if isinstance(result, dbus.String):
        try:
            json_result = json.loads(result)
            for item in json_result:
                logging.info(item)
            else:
                return True
        except json.JSONDecodeError:
            logging.info(f'返回数据不是json:{type(result)}')
            return False
    else:
        logging.info(f'返回数据类型不匹配:{type(result)}')
        return False


@checkword
def getJob(jobId):
    """
    GetJob(jobId int64) -> (string)
    根据 id 获取相应的 job。
    返回 job 的 json 字符串表示。
    :jobId:
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.GetJob(dbus.Int64(jobId))
    if isinstance(result, dbus.String):
        try:
            json_result = json.loads(result)
            logging.info(json_result)
            return True
        except json.JSONDecodeError:
            logging.info(f'返回数据不是json:{type(result)}')
            return False
    else:
        logging.info(f'返回数据类型不匹配:{type(result)}')
        return False


@checkword
def createJob():
    """
    CreateJob(jobInfo string) -> (id int64)
    jobInfo 为 job 的字符串表示。
    返回新 job 的 id。
    :return: True or False
    """
    job_info_dict = {"Type": 1, "Title": 'CreateJob', "Description": "", "AllDay": True,
                     "Start": f"{datetime.date.today().strftime('%Y-%m-%d')}T00:00:00+08:00",
                     "End": f"{datetime.date.today().strftime('%Y-%m-%d')}T23:59:00+08:00", "RRule": "",
                     "Remind": "1;09:00", "RecurID": 0,
                     "Ignore": []}

    job_info = json.dumps(job_info_dict)
    interface = dbus_interface()
    job_id = interface.CreateJob(job_info)
    if isinstance(job_id, dbus.Int64):
        return True
    else:
        logging.info(f'返回数据类型不匹配:{type(job_id)}')
        return False


@checkword
def updateJob(old_job_info, key='Title', value=f'UpdateJob{int(time.time())}'):
    """
    UpdateJob(jobInfo string)
    jobInfo 为 job 的字符串表示
    :return: True or False
    """
    old_job_info_dict = json.loads(old_job_info)
    old_job_info_dict[key] = value
    new_job_info = json.dumps(old_job_info_dict)
    interface = dbus_interface()
    interface.UpdateJob(new_job_info)
    return True


@checkword
def deleteJob(job_id):
    """
    DeleteJob(id int64)
    根据 id 删除相应的 job。
    :jobId: job id
    :return: True or False
    """
    interface = dbus_interface()
    interface.DeleteJob(dbus.Int64(job_id))
    return True


@checkword
def getTypes():
    """
    返回 job type 列表的 JSON 表示。
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.GetTypes()
    if isinstance(result, dbus.String):
        try:
            json_result = json.loads(result)
            logging.info(json_result)
            return True
        except json.JSONDecodeError:
            logging.info(f'返回数据不是json:{type(result)}')
            return False
    else:
        logging.info(f'返回数据类型不匹配:{type(result)}')
        return False


@checkword
def getType(type_id):
    """
    GetType(id int64) -> (string)
    返回 job type 的 JSON 表示。
    job type 具有的字段：

    ID int
    Name string
    Color string

    Name 名称，数据类型：字符串，不能为空。
    Color 颜色值，数据类型：字符串，不能为空，为 ”#“ 开头的十六进制颜色。
    :return: True or False
    """
    interface = dbus_interface()
    result = interface.GetType(dbus.Int64(type_id))
    if isinstance(result, dbus.String):
        try:
            json_result = json.loads(result)
            logging.info(json_result)
            return True
        except json.JSONDecodeError:
            logging.info(f'返回数据不是json:{type(result)}')
            return False
    else:
        logging.info(f'返回数据类型不匹配:{type(result)}')
        return False


@checkword
def createType():
    """
    CreateType(typeInfo string) -> (id int64)
    参数 typeInfo 为 job type 的 JSON 表示。
    返回新创建的 job type 的 id。
    :return: True or False
    """
    type_dict = {"ID": 1, "Name": "测试", "Color": "#FFF000"}
    logging.info(f"创建type,type_dict:{type_dict}")
    interface = dbus_interface()
    type_id = interface.CreateType(type_dict)
    if isinstance(type_id, dbus.Int64):
        return True
    else:
        logging.info(f'返回数据类型不匹配:{type(type_id)}')
        return False


def deleteType(type_id):
    """
    DeleteType(id int64) -> ()
    根据 id 删除相应的 job type。
    :return: True or False
    """
    interface = dbus_interface()
    interface.DeleteType(dbus.Int64(type_id))
    return True


def updateType(old_job_info, key='Name', value=f'updateType{int(time.time())}'):
    """
    UpdateType(typeInfo string) -> ()
    参数 typeInfo 为 job type 的 JSON 表示。
    :return: True or False
    """
    old_type_info_dict = json.loads(old_job_info)
    old_type_info_dict[key] = value
    new_type_info = json.dumps(old_type_info_dict)
    interface = dbus_interface()
    interface.UpdateType(new_type_info)
    return True


@checkword
def getJobsWithLimit():
    """
    GetJobsWithLimit(int32 startYear, int32 startMonth, int32 startDay,
                     int32 endYear, int32 endMonth, int32 endDay , int32 maxNum) -> (string jobs)
    根据一个时间段的起始范围，以及需要的最大日程数量，返回需要的日程，返回的字符串为JSON格式字符串
    :return: True or False
    """
    year = datetime.date.today().year
    interface = dbus_interface()
    result = interface.GetJobsWithLimit(dbus.Int32(year), dbus.Int32(1), dbus.Int32(1),
                                        dbus.Int32(year), dbus.Int32(12), dbus.Int32(31), dbus.Int32(100))
    if isinstance(result, dbus.String):
        if dbus.String('null') == result:
            return True
        else:
            try:
                json_result = json.loads(result)
                for item in json_result:
                    logging.info(item)
            except json.JSONDecodeError:
                logging.info(f'返回数据不是json:{type(result)}')
                return False
    else:
        logging.info(f'返回数据类型不匹配:{type(result)}')
        return False


@checkword
def getJobWithRule(rule=None):
    """
    GetJobsWithRule(int32 startYear, int32 startMonth, int32 startDay,
                    int32 endYear, int32 endMonth, int32 endDay , string rule) -> (string jobs)
    根据一个时间段的起始范围，以及日程的重复类型，返回需要的日程，返回的字符串为JSON格式字符串,
    目前共有五种重复类型：每日("FREQ=DAILY")，工作日("FREQ=DAILY;BYDAY=MO,TU,WE,TH,FR"),
    每周("FREQ=WEEKLY")，每月("FREQ=MONTHLY")，每年("FREQ=YEARLY")
    @return: True or False
    """
    if rule is None:
        rule = "DAILY"
    year = datetime.date.today().year
    interface = dbus_interface()
    result = interface.GetJobsWithRule(dbus.Int32(year), dbus.Int32(1), dbus.Int32(1),
                                       dbus.Int32(year), dbus.Int32(12), dbus.Int32(31), dbus.String(rule))
    if isinstance(result, dbus.String):
        if dbus.String('null') == result:
            return True
        else:
            try:
                json_result = json.loads(result)
                for item in json_result:
                    logging.info(item)
            except json.JSONDecodeError:
                logging.info(f'返回数据不是json:{type(result)}')
                return False
    else:
        logging.info(f'返回数据类型不匹配:{type(result)}')
        return False
