# -*- coding: utf-8 -*-
import time
import json
import datetime
import logging

import dbus

from aw.dbus.dbus_common import get_session_dbus_interface
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.api.LunarCalendar'
DBUS_PATH = '/com/deepin/api/LunarCalendar'
IFACE_NAME = 'com.deepin.api.LunarCalendar'


def dbus_interface():
    return get_session_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


@checkword
def getFestivalMonth():
    """
    GetFestivalMonth (int32 year, int32 month) -> (String json),获取指定公历月的假日信息
    参数
        year: 公历年
        mouth: 公历月
    返回
        json：指定公历月的假日信息,JSON 格式，比如：
                                [
                                    {
                                        "id": "2020062506",
                                        "name": "端午节",
                                        "description": "6月25日至6月27日放假3天，6月28日上班",
                                        "rest": "2020年6月22日至2020年6月24日请假3天，与周末连休可拼8天长假。",
                                        "month": 6,
                                        "list": [
                                            {
                                                "date": "2020-6-25",
                                                "status": 1
                                            }, {
                                                "date": "2020-6-26",
                                                "status": 1
                                            }, {
                                                "date": "2020-6-27",
                                                "status": 1
                                            }, {
                                                "date": "2020-6-28",
                                                "status": 2
                                            }
                                        ]
                                    }
                                ]
        JSON 说明:
            最外层是个数组,数组中每个元素都是 Festival 对象
            Festival 对象:
            struct {
                string ID
                string Name
                string Description
                string Rest
                int Month
                HolidayList Holidays
            }

            ID:节假日id，包含日期内容
            Name:节假日名
            Description:放假和补班的描述
            Rest:拼假建议
            Month:节日月份
            Holidays: 放假与补班日期的数组，数组中每个元素都是 Holiday 对象

        Holiday 对象:
            struct {
                string Date
                HolidayStatus Status
            }

            Date:日期
            Status:状态，值为1时，放假;值为2时，上班;
    :return:
    """
    year = datetime.date.today().year
    month = datetime.date.today().month
    logging.info(f"查询{year}年{month}月")
    interface = dbus_interface()
    result = interface.GetFestivalMonth(dbus.Int32(year), dbus.Int32(month))
    if isinstance(result, dbus.String):
        try:
            json_result = json.loads(result)
            if json_result:
                for item in json_result:
                    logging.info(item)
                else:
                    return True
            else:
                logging.info(f"{year}年{month}月没有节日信息")
                return True
        except json.JSONDecodeError:
            logging.info(f'返回数据不是json:{type(result)}')
            return False
    else:
        logging.info(f'返回数据类型不匹配:{type(result)}')
        return False


@checkword
def getFestivalsInRange():
    """
    GetFestivalsInRange (string startDate, string endDate) -> ([]DayFestival result),获取一段时间内的节假日信息
    参数
        startDate:开始日期,例如: 20200101
        endDate:结束日期,例如: 20201010
    返回
        result:节假日信息，是一个数组，每个元素都是 DayFestival 对象.
        DayFestival 对象:
                struct {
                    int32 Year
                    int32 Month
                    int32 Day
                    []string Festivals
                }
                Year:公历年
                Month:公历月
                Day:公历日
        Festivals:节假日
    :return:
    """
    today = datetime.date.today()
    endday = datetime.date.today() + datetime.timedelta(30)
    s_today = today.strftime("%Y%m%d")
    s_endday = endday.strftime("%Y%m%d")
    logging.info(f"查询{s_today}到{s_endday}")

    interface = dbus_interface()
    result = interface.GetFestivalsInRange(dbus.String(today), dbus.String(endday))
    if isinstance(result, dbus.Array):
        if result:
            for item in result:
                logging.info(item)
            else:
                return True
        else:
            logging.info(f"{s_today}到{s_endday}没有节日信息")
            return True

    else:
        logging.info(f'返回数据类型不匹配:{type(result)}')
        return False


@checkword
def getHuangLiDay():
    """
    GetHuangLiDay (int32 year, int32 month, int32 day) -> (string json),获取指定公历日的黄历信息
    参数
        year:公历年
        month:公历月
        day:公历日
    返回
        json:指定公历日的黄历信息,JSON 格式，比如：
                {
                    "GanZhiYear": "庚子",
                    "GanZhiMonth": "辛巳",
                    "GanZhiDay": "庚戌",
                    "LunarMonthName": "四月",
                    "LunarDayName": "十五",
                    "LunarLeapMonth": 0,
                    "Zodiac": "鼠",
                    "Term": "",
                    "SolarFestival": "",
                    "LunarFestival": "",
                    "Worktime": 0,
                    "Avoid": "移徙.入宅.造屋.架马.",
                    "Suit": "嫁娶.纳采.订盟.斋醮.开光.祭祀.祈福.求医.治病.会亲友.动土.解除.捕捉.纳畜.牧养.入殓.破土.安葬."
                }
        JSON 说明:是一个 HuangLiInfo 对象.
        HuangLiInfo 对象:
            struct {
                calendar.LunarDayInfo
                string Avoid
                string Suit
            }
            LunarDayInfo: 农历信息
            Avoid:黄历 忌
            Suit:黄历 宜

        LunarDayInfo 对象:
            struct {
                string GanZhiYear
                string GanZhiMonth
                string GanZhiDay
                string LunarMonthName
                string LunarDayName
                int32  LunarLeapMonth
                string Zodiac
                string Term
                string SolarFestival
                string LunarFestival
                int32  Worktime
            }
            字段含义:
                GanZhiYear: 农历年的干支
                GanZhiMonth: 农历月的干支
                GanZhiDay: 农历日的干支
                LunarMonthName: 农历月名
                LunarDayName: 农历日名
                LunarLeapMonth: 未使用
                Zodiac: 农历年的生肖
                Term: 农历节气
                SolarFestival: 公历节日
                LunarFestival: 农历节日
                Worktime: 未使用

    报错
    invalid date: 无效的日期
    输入参数错误，日期无效

    :return:
    """
    year = datetime.date.today().year
    month = datetime.date.today().month
    day = datetime.date.today().day
    logging.info(f"查询{year}年{month}月{day}日")
    interface = dbus_interface()
    result = interface.GetHuangLiDay(dbus.Int32(year), dbus.Int32(month), dbus.Int32(day))

    if isinstance(result, dbus.String):
        try:
            json_result = json.loads(result)
            if json_result:
                for key in json_result:
                    logging.info(f"{key}:{json_result[key]}")
                else:
                    return True
            else:
                logging.info(f"{year}年{month}月没有节日信息")
                return True
        except json.JSONDecodeError:
            logging.info(f'返回数据不是json:{type(result)}')
            return False
    else:
        logging.info(f'返回数据类型不匹配:{type(result)}')
        return False


@checkword
def getHuangLiMonth(fill=False, rasie_invalid=False):
    """
    GetHuangLiMonth(int32 year, int32 month, bool fill) -> (string json),获取指定公历月的黄历信息
    参数
        year:公历年
        month:公历月
        fill:是否用上下月数据补齐首尾空缺，首例数据从周日开始
    返回
        json:指定公历月的黄历信息,JSON 格式，比如：
                {
                    "FirstDayWeek": 1,
                    "Days": 30,
                    "Datas": [{
                        "GanZhiYear": "庚子",
                        "GanZhiMonth": "辛巳",
                        "GanZhiDay": "甲戌",
                        "LunarMonthName": "闰四月",
                        "LunarDayName": "初九",
                        "LunarLeapMonth": 0,
                        "Zodiac": "鼠",
                        "Term": "",
                        "SolarFestival": "",
                        "LunarFestival": "",
                        "Worktime": 0,
                        "Avoid": "嫁娶.上梁.修造.拆卸.架马.入宅.伐木.动土.出火.开柱眼.",
                        "Suit": "祭祀.开光.出行.解除.塑绘.裁衣.入殓.移柩.破土.启攒.安葬.除服.成服."
                    }, {
                        "GanZhiYear": "庚子",
                        "GanZhiMonth": "辛巳",
                        "GanZhiDay": "乙亥",
                        "LunarMonthName": "闰四月",
                        "LunarDayName": "初十",
                        "LunarLeapMonth": 0,
                        "Zodiac": "鼠",
                        "Term": "",
                        "SolarFestival": "儿童节",
                        "LunarFestival": "",
                        "Worktime": 0,
                        "Avoid": "诸事不宜.",
                        "Suit": "祭祀.解除.破屋.坏垣.余事勿取."
                    }...]
                }
        JSON 说明:是一个 HuangLiMonthInfo 对象.
        HuangLiMonthInfo 对象:
            struct {
                int32 FirstDayWeek
                int32 Days
                HuangLiInfoList Datas
            }
            FirstDayWeek: 该月第一天是周几
            Days: 该月有多少天
            Datas:黄历信息，是一个数组，数组每个元素都是一个 HuangLiInfo 对象

    报错
        invalid date: 无效的日期
        输入参数错误，日期无效

    :return:
    """
    year = datetime.date.today().year
    if rasie_invalid:
        month = 13
    else:
        month = datetime.date.today().month
    logging.info(f"查询{year}年{month}月")
    interface = dbus_interface()
    try:
        result = interface.GetHuangLiMonth(dbus.Int32(year), dbus.Int32(month), dbus.Boolean(fill))
        if rasie_invalid:
            logging.info("未引发invalid date错误")
            return False

    except dbus.DBusException as e:
        dbus_message = dbus.DBusException.get_dbus_message(e)
        if rasie_invalid and "invalid date" in dbus_message:
            return True
        raise e

    if isinstance(result, dbus.String):
        try:
            json_result = json.loads(result)
            if json_result:
                for key in json_result:
                    if dbus.String(key) == "Datas":
                        for itme in json_result[key]:
                            logging.info(itme)
                    else:
                        logging.info(f"{key}:{json_result[key]}")
                    return True
            else:
                logging.info(f"{year}年{month}月没有节日信息")
                return True
        except json.JSONDecodeError:
            logging.info(f'返回数据不是json:{type(result)}')
            return False
    else:
        logging.info(f'返回数据类型不匹配:{type(result)}')
        return False


@checkword
def getLunarInfoBySolar():
    """
    GetLunarInfoBySolar(int32 year,int32 month,int32 day) -> (calendar.LunarDayInfo lunarDay, bool ok)
    获取指定公历日期的农历信息
    参数
        year: 公历年
        month: 公历月
        day: 公历日
    返回
        lunarDay: 农历信息,是一个 LunarDayInfo 对象
        ok: 获取是否成功
    :return:
    """
    year = datetime.date.today().year
    month = datetime.date.today().month
    day = datetime.date.today().day
    logging.info(f"查询{year}年{month}月{day}日")
    interface = dbus_interface()
    result, ok = interface.GetLunarInfoBySolar(dbus.Int32(year), dbus.Int32(month), dbus.Int32(day))
    if isinstance(ok, dbus.Boolean):
        logging.info(f"ok:{ok}")
    else:
        logging.info(f'返回数据类型不匹配,ok:{type(ok)}')
        return False

    if isinstance(result, dbus.Struct):
        logging.info(f"result:{result}")
        return True
    else:
        logging.info(f'返回数据类型不匹配,result:{type(result)}')
        return False


@checkword
def getLunarMonthCalendar(fill=False):
    """
    GetLunarMonthCalendar(int32 year,int32 month,bool fill) -> (LunarMonthInfo lunarMonth, bool ok)
    获取指定指定公历月份的农历信息
    参数
        year: 公历年
        month: 公历月
        fill: 是否用上下月数据补齐首尾空缺，首例数据从周日开始
    返回
        lunarMonth:农历信息,是一个 LunarMonthInfo 对象
        ok:获取是否成功

        LunarMonthInfo 对象:
            struct {
                int32 FirstDayWeek
                int32 Days
                []calendar.LunarDayInfo Datas
            }
        FirstDayWeek: 该月第一天是周几
        Days: 该月有多少天
        Datas:黄历信息，是一个数组，数组每个元素都是一个 LunarDayInfo 对象
    报错
        无
    :return:
    """
    year = datetime.date.today().year
    month = datetime.date.today().month
    logging.info(f"查询{year}年{month}月")
    interface = dbus_interface()
    result, ok = interface.GetLunarMonthCalendar(dbus.Int32(year), dbus.Int32(month), dbus.Boolean(fill))
    if isinstance(ok, dbus.Boolean):
        logging.info(f"ok:{ok}")
    else:
        logging.info(f'返回数据类型不匹配,ok:{type(ok)}')
        return False

    if isinstance(result, dbus.Struct):
        logging.info(f"FirstDayWeek:{result[0]}")
        logging.info(f"Days:{result[1]}")
        for item in result[2]:
            logging.info(f"LunarDayInfo:{item}")
        else:
            return True

    else:
        logging.info(f'返回数据类型不匹配,result:{type(result)}')
        return False
