#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import xml.dom.minidom
import logging
from frame import constant


class OSBase(unittest.TestCase):

    def Step(self, num):
        str_ = "=" * 20 + "{}".format(num) + "=" * 30
        logging.info(str_)

    def CheckPoint(self, num):
        str_ = "=" * 20 + "{}".format(num) + "=" * 30
        logging.info(str_)

    def get_data(self, node):
        '''
        获取配置文件参数
        '''
        dom = xml.dom.minidom.parse(constant.data_config_path)
        root = dom.documentElement
        node_list = root.getElementsByTagName(node)
        node_ = node_list[0].firstChild.data
        data_ = str(node_)
        return data_
