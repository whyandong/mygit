# -*- coding:utf-8 -*-
import logging
import re
import time
import dbus

from aw.common import excute_cmd
from frame.decorator import checkword
from subprocess import getstatusoutput

DBUS_NAME = 'com.deepin.daemon.PasswdConf'
DBUS_PATH = '/com/deepin/daemon/PasswdConf'
IFACE_NAME = 'com.deepin.daemon.PasswdConf'


# ===========================
#         功能函数
# ===========================
def system_bus(dbus_name=DBUS_NAME, dbus_path=DBUS_PATH,
               iface_name=IFACE_NAME):
    system_bus = dbus.SystemBus()
    system_obj = system_bus.get_object(dbus_name, dbus_path)
    property_obj = dbus.Interface(system_obj, dbus_interface=iface_name)
    return property_obj

# def get_properties_value(properties: str):
#     property_obj = get_system_dbus_interface(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
#     result = property_obj.Get(IFACE_NAME, properties)
#     return result

def cmd_input(passwd, dbus_name=DBUS_NAME, dbus_path=DBUS_PATH, dbus_iface=None):
    #cmd = 'sudo dbus-send --system --print-reply  --dest={} {} {}'.format(dbus_name, dbus_path, dbus_iface)
    cmd = f'echo {passwd} | sudo -S dbus-send --system --print-reply  --dest={dbus_name} {dbus_path} {dbus_iface}'
    time.sleep(1)
    logging.info(cmd)
    (status, output) = getstatusoutput(cmd)
    output_ = output.split('string')[-1]
    # logging.info(output)
    if status == 0:
        logging.info(f'命令执行成功{status}')
        return output_
    else:
        logging.info(f'命令执行失败{status}')
        return status

def getLength():
    """
    获取密码检验配置中的最大和最小长度限制
    :return:Int32 minLength, Int32 maxLength
    """
    interface = system_bus()
    length = interface.GetLengthLimit()
    logging.info(length)
    return length

def getPolicy():
    """
    获取当前用户密码检验策略信息
    :return:dbus.String
    """
    interface = system_bus()
    result = interface.GetValidatePolicy()
    logging.info(result)
    return result

def getRequired():
    """
    设置密码校验配置中的强度策略信息
    """
    interface = system_bus()
    result = interface.GetValidateRequired()
    logging.info(result)
    return result

def getFirstLetterUpper():
    """
    获取密码首字母是否需要大写的配置信息状态
    """
    interface = system_bus()
    result = interface.GetFirstLetterUpper()
    logging.info(result)
    return result

def setLengthLimit(passwd, data):
    """
    设置密码校验配置中的长度限制，自定义一组参数值
    :params: Int32 minLength, Int32 maxLength
    :return: 无
    """
    cmd_input(passwd, dbus_iface='com.deepin.daemon.PasswdConf.SetLengthLimit int32:{} int32:{}'.format(data[0], data[1]))
    return True

def setValidatePolicy(passwd, data):
    """
    设置密码检验策略配置
    params: passwd: 用户管理密码鉴权; data: 自定义密码检验策略信息
    :return: 无
    """
    cmd_input(passwd, dbus_iface='com.deepin.daemon.PasswdConf.SetValidatePolicy string:"{}"'.format(data))
    return True

def setValidateRequired(passwd, data):
    """
    设置密码校验配置中的强度策略，使用自定义策略信息写入
    :params: passwd: 用户管理密码鉴权; data: 自定义密码强度策略信息
    :return: 无
    """
    cmd_input(passwd, dbus_iface='com.deepin.daemon.PasswdConf.SetValidateRequired int32:{}'.format(data))
    return True

def setFirstLetterUpper(passwd, status):
    """
    设置首字母是否需要大写的配置，使用自定义状态写入
    :params: passwd: 用户管理密码鉴权; status: 自定义密码强度策略信息
    :return: 无
    """
    if status == 0:
        status = 'false'
    elif status == 1:
        status = 'true'
    cmd_input(passwd, dbus_iface='com.deepin.daemon.PasswdConf.SetFirstLetterUpper boolean:{}'.format(status))
    return True

def getEnabled():
    """
    获取密码校验配置信息或状态
    :return:Boolean
    """
    interface = system_bus()
    result = interface.GetEnabled()
    logging.info(result)
    return result

def readConfig(passwd):
    """
    获取密码策略配置信息
    :return:string
    """
    result = cmd_input(passwd, dbus_iface='com.deepin.daemon.PasswdConf.ReadConfig')
    logging.info(result)
    return result

def backup(passwd):
    """
    执行当前密码策略配置的备份
    :return:无
    """
    cmd_input(passwd, dbus_iface='com.deepin.daemon.PasswdConf.Backup')

def reset(passwd):
    """
    获取密码策略配置
    :return:string
    """
    cmd_input(passwd, dbus_iface='com.deepin.daemon.PasswdConf.Reset')

@checkword
def setEnabled(passwd, mode):
    """
    获取密码检验配置中的最大和最小长度限制
    :params: Int32 minLength, Int32 maxLength
    :return: 无
    """
    if mode == 0:
        mode = 'false'
    elif mode == 1:
        mode = 'true'
    cmd_input(passwd, dbus_iface='com.deepin.daemon.PasswdConf.SetEnabled boolean:{}'.format(mode))
    return True

@checkword
def read_Config(passwd):
    """
    获取密码策略配置，并校对关键参数是否存在
    :return:string
    """
    list_ = ['Password', 'STRONG_PASSWORD', 'VALIDATE_POLICY', 'VALIDATE_REQUIRED', 'FIRST_LETTER_UPPERCASE']
    result = readConfig(passwd)
    for i in list_:
        if not re.findall(i, result):
            logging.info(f'返回密码策略参数缺失,返回值为{i}')
            return False
    if isinstance(result, str):
        logging.info('返回密码策略参数和数据类型为dbus.String正常')
        return True
    else:
        logging.info(f'返回密码数据类型为dbus.String异常,返回值类型为{type(result)}')
        return False

@checkword
def get_Enabled():
    """
    获取密码校验配置是否使用
    :return:Boolean
    """
    result = getEnabled()
    if isinstance(result, dbus.Boolean):
        logging.info('返回密码配置数据类型为dbus.Boolean正常')
        return True
    else:
        logging.info(f'返回密码配置数据类型异常,返回值类型为{type(result)}')
        return False

@checkword
def set_Enabled(passwd, mode):
    """
    获取密码校验配置信息，根据不同模式，校验两种状态设置是否生效
    :return:Boolean
    """
    if mode == 'enable':
        setEnabled(passwd, 'true')
        result = system_bus().GetEnabled()
        logging.info(result)
        if isinstance(result, dbus.Boolean) and result:
            logging.info('返回密码校验配置数据类型为dbus.Boolean正常')
            return True
        else:
            logging.info(f'返回密码校验配置数据类型异常,返回值类型为{type(result)}')
            return False
    elif mode == 'disable':
        setEnabled(passwd, 'false')
        result = system_bus().GetEnabled()
        logging.info(result)
        if isinstance(result, dbus.Boolean) and not result:
            logging.info('返回密码校验配置数据类型为dbus.Boolean正常')
            return True
        else:
            logging.info(f'返回密码校验配置数据类型异常,返回值类型为{type(result)}')
            return False
    else:
        logging.info(f'密码校验配置模式类型异常,返回值为{mode}')
        return False

@checkword
def get_FirstLetterUpper():
    """
    获取首字母是否需要大写的配置信息
    :return:Boolean
    """
    interface = system_bus()
    result = interface.GetFirstLetterUpper()
    logging.info(result)
    if isinstance(result, dbus.Boolean):
        logging.info('返回密码首字母数据类型为dbus.Boolean正常')
        return True
    else:
        logging.info(f'返回密码首字母数据类型异常,返回值类型为{type(result)}')
        return False

@checkword
def getLengthLimit():
    """
    获取密码检验强度配置中的最小和最大长度限制，保证长度大于0,且最大长度大于最小长度
    :return:Int32 minLength, Int32 maxLength
    """
    interface = system_bus()
    length = interface.GetLengthLimit()
    logging.info(length)
    if length[0] > 0 and length[0] < length[1]:
        logging.info("返回密码限制长度数据类型为dbus.Int32正常，且最大长度大于最小长度")
        return True
    else:
        logging.info(f'返回密码限制长度类型异常或设置不合理,返回值类型为{type(length[0])}，{type(length[1])}')
        return False

@checkword
def getValidatePolicy():
    """
    获取密码校验配置中的策略信息，各策略信息长度大于0
    :return:dbus.String
    """
    interface = system_bus()
    result = interface.GetValidatePolicy()
    logging.info(result)
    if isinstance(result, dbus.String):
        list_ = list(result.split(';'))
        for i in list_:
            if len(i) > 0:
                pass
            else:
                logging.info(f'部分密码策略信息长度为空，不合理')
                return False
        logging.info("返回密码策略信息类型为dbus.String正常，且各策略值长度正常")
        return True
    else:
        logging.info(f'返回密码策略信息类型异常,返回值类型为{type(result)}')
        return False

@checkword
def getValidateRequired():
    """
    获取密码校验配置中的强度策略，策略参数值大于0
    :return:dbus.Int32
    """
    interface = system_bus()
    result = interface.GetValidateRequired()
    logging.info(result)
    if isinstance(result, dbus.Int32) and result >= 0:
        logging.info("返回密码强度策略类型为dbus.Int32正常")
        return True
    else:
        logging.info(f'返回密码强度策略类型或值异常,返回类型为{type(result)}')
        return False

@checkword
def checklengthConfig(length):
    """
    校验密码策略配置中的长度限制值，与原自定义数据值对比，写入是否生效
    :params: Int32 minLength, Int32 maxLength
    :return: 无
    """
    lenth_ = getLength()
    for i in range(len(lenth_)):
        if isinstance(lenth_[i], dbus.Int32):
            if lenth_[i] == length[i]:
                pass
            else:
                logging.info(f"写密码策略长度限制配置未生效，当前返回值为{lenth_[i]}")
                return False
        else:
            logging.info(f"写密码策略长度限制配置数据类型异常,返回值类型为{type(lenth_[i])}")
            return False
    logging.info("写密码策略长度限制配置正常，数据类型为dbus.String正常")
    return True

@checkword
def checkValidatePolicy(data):
    """
    校验密码检验策略配置信息，与原自定义参数信息分别对比，写入是否生效
    :params: data：原自定义密码检验策略信息
    :return: 无
    """
    result = getPolicy()
    if isinstance(result, dbus.String):
        if result == data:
            logging.info("写密码检验策略配置正常，数据类型为dbus.String正常")
            return True
        else:
            logging.info(f"写密码检验策略配置未生效，当前返回值为{result}")
            return False
    else:
        logging.info(f"写密码检验策略配置数据类型异常,返回值类型为{type(result)}")
        return False

@checkword
def checkValidateRequired(data):
    """
    校验密码强度策略配置信息，与原自定义参数信息分别对比，写入是否生效
    :params: data：原自定义密码检验策略信息
    :return: 无
    """
    result = getRequired()
    if isinstance(result, dbus.Int32):
        if result == data:
            logging.info("写密码强度策略配置正常，数据类型为dbus.String正常")
            return True
        else:
            logging.info(f"写密码强度策略配置未生效，当前返回值为{result}")
            return False
    else:
        logging.info(f"写密码强度策略配置数据类型异常,返回值类型为{type(result)}")
        return False

@checkword
def checkFirstLetterUpper(status):
    """
    校验密码首字母大小写状态信息，与原自定义参数信息分别对比，写入是否生效
    :params: status：原自定义密码首字母大小写状态信息: false
    :return: 无
    """
    # result = getFirstLetterUpper()
    interface = system_bus()
    result = interface.GetFirstLetterUpper()
    if isinstance(result, dbus.Boolean):
        if not result:
            logging.info("写密码首字母状态配置正常，数据类型为dbus.String正常")
            return True
        else:
            logging.info(f"写密码首字母状态配置未生效，当前返回值为{result}")
            return False
    else:
        logging.info(f"写密码首字母状态配置数据类型异常,返回值类型为{type(result)}")
        return False

@checkword
def writeConfig(passwd, data):
    """
    密码校验策略配置写入dde.conf
    :return:无
    """
    result = cmd_input(passwd, dbus_iface='com.deepin.daemon.PasswdConf.WriteConfig string:"{}"'.format(data))
    logging.info(result)
    return True

@checkword
def checkpwdConfig(passwd, data):
    """
    获取密码策略配置，并校验数据类型，对比原写入密码信息是否一致
    :return:string
    """
    pwdconf = readConfig(passwd)
    if isinstance(pwdconf, str):
        if data in pwdconf:
            logging.info("写密码策略配置正常，数据类型为dbus.String正常")
            return True
        else:
            logging.info(f'写密码策略配置数据未成功')
            return False
    else:
        logging.info(f'写密码配置数据类型异常,返回值类型为{type(pwdconf)}')
        return False

@checkword
def checkresetConfig(passwd):
    """
    获取密码策略配置信息，校验数据类型，与备份密码策略数据是否一致
    :return:string
    """
    pwdconf = readConfig(passwd)
    cmd = 'cat /etc/deepin/dde.conf.bak'
    out = excute_cmd(cmd)
    logging.info(out)
    if isinstance(pwdconf, str) and out in pwdconf:
        logging.info("重置密码策略配置正常，数据类型为dbus.String正常")
        return True
    else:
        logging.info(f'重置密码策略配置数据失败或类型异常,返回值类型为{type(pwdconf)}')
        return False

@checkword
def checkbackupConfig(passwd):
    """
    获取密码策略配置信息，校验数据类型，文件内容，更新生效时间（误差5秒内)
    :return:string
    """
    pwdconf = readConfig(passwd)
    cmd = 'cat /etc/deepin/dde.conf.bak'
    cmd1 = 'stat -c %Y /etc/deepin/dde.conf.bak'
    out = excute_cmd(cmd)
    baktime = excute_cmd(cmd1)
    time2 = time.time()
    logging.info(out)
    if isinstance(pwdconf, str) and out in pwdconf:
        if int(time2) - int(baktime) < 5:
            logging.info("备份密码策略配置文件成功，数据类型为dbus.String正常")
            return True
        else:
            logging.info(f"备份密码策略配置文件不成功，当前备份时间为{baktime}")
            return False
    else:
        logging.info(f"备份密码策略配置数据类型异常,返回值类型为{type(pwdconf)}")
        return False