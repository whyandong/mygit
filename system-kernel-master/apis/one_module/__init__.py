# -*- coding: utf-8 -*-
import os

from frame.decorator import check_word
from frame.get_config import GetXmlConfig
from frame.constant import configs_root_path


@check_word(target=1)
def module_one():
    return 1


def get_config():
    config_path = os.path.join(configs_root_path, "data_config.xml")
    config = GetXmlConfig(config_path)
    return config
