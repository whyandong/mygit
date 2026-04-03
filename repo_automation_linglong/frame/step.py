# -*- coding: utf-8 -*-
"""
@Time ： 2021/8/5 下午5:28
@Auth ： lizhouquan
@File ：step.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)

"""

from frame.projectLog import log
logger=log()
def Step(num):
    str_ = "=" * 20 + "{}".format(num) + "=" * 30
    logger.info(str_)
