# -*- coding: utf-8 -*-
import os
import logging
import time

from frame.decorator import checkword
from aw.dbus.systemBus import systemCommon

dbus_name = 'com.deepin.daemon.ImageEffect'
dbus_path = '/com/deepin/daemon/ImageEffect'
iface_name = 'com.deepin.daemon.ImageEffect'


def get(effect, filename):
    """
    将图片根据需求特效,生成图片
    :param effect:特效
    :param filename:文件名
    :return:str
    """
    picture_type = ['.jpg', '.bmp']
    if not os.path.exists(filename):
        picture_path = os.path.splitext(filename)[0]
        for item in picture_type:
            picture_file_path = f"{picture_path}{item}"
            if os.path.exists(picture_file_path):
                filename = picture_file_path
                logging.info(f"{filename}")
                break
        else:
            logging.info('未找到相关图片')
            raise RuntimeError('未找到相关图片')

    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    dbus_out = property_obj.Get(effect, filename)
    return dbus_out


@checkword
def getImageEffect(effect, filename):
    """
    将图片根据需求特效,生成图片,并检查生成图片成功
    :param effect:特效
    :param filename:文件名
    :return:True or False
    """
    ret = get(effect, filename)
    logging.info(ret)
    if '/var/cache/deepin/dde-daemon/image-effect/pixmix' in ret:
        logging.info("将图片根据需求特效,生成图片成功")
        return True
    else:
        logging.info("将图片根据需求特效,生成图片失败")
        return False


@checkword
def delete(effect, filename):
    """
    根据效果和图片名,删除生成的文件
    :param effect:特效
    :param filename:文件名
    :return:None
    """
    picture_type = ['.jpg', '.bmp']
    if not os.path.exists(filename):
        picture_path = os.path.splitext(filename)[0]
        for item in picture_type:
            picture_file_path = f"{picture_path}{item}"
            if os.path.exists(picture_file_path):
                filename = picture_file_path
                logging.info(f"{filename}")
                break
        else:
            logging.info('未找到相关图片')
            raise RuntimeError('未找到相关图片')

    ret = get(effect, filename)
    out = ret.split('/')[-1]
    logging.info(out)
    time.sleep(2)

    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    property_obj.Delete(effect, filename)

    item = systemCommon.excute_cmd('ls /var/cache/deepin/dde-daemon/image-effect/pixmix')
    if out not in item:
        logging.info("将图片根据需求特效,删除生成的文件成功")
        return True
    else:
        logging.info("将图片根据需求特效,删除生成的文件失败")
        return False
