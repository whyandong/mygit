import logging
import os
import time
import datetime
nowtime = time.strftime("%Y-%m-%d")
def log():
    #创建logger，如果参数为空则返回root
    logger=logging.getLogger("更新平台")
    #设置日志等级
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        #创建handler
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../log/webpublic')
        test_data_path = os.path.abspath( path +"Metis_{}.log".format(nowtime))

        fh=logging.FileHandler(test_data_path,encoding="utf-8")
        ch=logging.StreamHandler()

        #设置日志输出格式
        formatter = logging.Formatter(
            fmt="%(asctime)s %(name)s %(levelname)s %(message)s ",
            datefmt='%Y-%m-%d  %H:%M:%S %a ')

        #为handler指定输出格式
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        #为logger添加的日志处理器
        logger.addHandler(fh)
        logger.addHandler(ch)
        fh.close()
    return logger
