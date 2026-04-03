# -*- coding: utf-8 -*-
import sys
sys.path.append(r"/home/sun870/uniontest-master/uniontest-master/deepin-elf-sign-tool/") 
import logging
import xml.dom.minidom


class GetXmlConfig:

    def __init__(self, xml_file):
        dom_tree = xml.dom.minidom.parse(xml_file)
        self.collection = dom_tree.documentElement

    def get_int(self, item):
        try:
            node = self.collection.getElementsByTagName(item)[0]
            return int(node.childNodes[0].data)
        except Exception as e:
            logging.exception(e)
            return None

    def get_str(self, item):
        try:
            node = self.collection.getElementsByTagName(item)[0]
            return str(node.childNodes[0].data)
        except Exception as e:
            logging.exception(e)
            return None

    def get_list(self, item):
        try:
            nodes = self.collection.getElementsByTagName(item)
            return [node.childNodes[0].data for node in nodes]
        except Exception as e:
            logging.exception(e)
            return None


if __name__ == "__main__":
    c = GetXmlConfig("../configs/data_config.xml")
    print(c.get_int("passwd"), type(c.get_int("passwd")))
    print(c.get_str("passwd"), type(c.get_str("passwd")))
    print(c.get_list("passwd"), type(c.get_list("passwd")))