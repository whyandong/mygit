# -*- coding: utf-8 -*-
"""日志模块"""

import os
from functools import wraps
import logbook
from logbook.more import ColorizedStderrHandler


def log_type(record, handler):
    log = "[{date}] [{level}] [{filename}] [{func_name}] [{lineno}] {msg}".format(
        date=record.time,  # 日志时间
        level=record.level_name,  # 日志等级
        filename=os.path.split(record.filename)[-1],  # 文件名
        func_name=record.func_name,  # 函数名
        lineno=record.lineno,  # 行号
        msg=record.message  # 日志内容
    )
    return log


def create_log_path():
    """
    创建日志文件夹
    """
    check_path = os.getcwd()
    LOG_DIR = os.path.join(check_path, 'logdir')
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    return LOG_DIR


def get_logger(name='jiekou', level=''):
    """ 
    日志配置
    """
    logbook.set_datetime_format('local')
    logger = logbook.Logger(name)
    logger.handlers = []
    logStd = ColorizedStderrHandler(bubble=False, level=level)
    logStd.formatter = log_type
    logFile = logbook.TimedRotatingFileHandler(os.path.join(
        create_log_path(), '%s.log' % name),
                                               date_format='%Y-%m-%d-%H',
                                               bubble=True,
                                               encoding='utf-8',
                                               backup_count=3)
    logFile.formatter = log_type
    logger.handlers.append(logFile)
    logger.handlers.append(logStd)
    return logger


def logger(param):
    """
    日志装饰器
    """

    def wrap(function):

        @wraps(function)
        def _wrap(*args, **kwargs):
            """ wrap tool """
            LOG.info("当前模块 {}".format(param))
            LOG.info("全部args参数参数信息 , {}".format(str(args)))
            LOG.info("全部kwargs参数信息 , {}".format(str(kwargs)))
            return function(*args, **kwargs)

        return _wrap

    return wrap


LOG = get_logger(level='INFO')

if __name__ == '__main__':
    LOG.info('接口测试')
