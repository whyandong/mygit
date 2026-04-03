# -*- coding: utf-8 -*-
import sys
sys.path.append(r"/home/sun870/uniontest-master/uniontest-master/deepin-elf-sign-tool/") 
import os
from frame import constant



def get_case():
    """
    获取用例
    :return:case_list
    """
    if os.path.exists(constant.execute_file):
        path_ = constant.execute_file
    else:
        path_ = os.path.join(constant.root_path, "excute.txt")

    with open(path_, 'r') as f:
        content_list = f.readlines()
        tmp_list = []
        for line in content_list:
            if line.strip():
                if line.startswith('/'):
                    tmp_list.append(line.strip()[1:])
                else:
                    tmp_list.append(line.strip())

        case_list = [os.path.join(constant.root_path, line) for line in tmp_list]
        f.close()

    return case_list


def get_skip_list():

    skip_list = []
    with open(constant.skip_list_file, mode='r', encoding='utf8') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('#'):
                continue
            elif line.strip():
                _ = line.strip()
                if _.startswith('/'):
                    skip_list.append(_[1:])
                else:
                    skip_list.append(_)

    return skip_list


def get_case_file_list():
    case_file_list = []
    for dirname, subdirs, files in os.walk(constant.script_root_path):

        files.sort()

        for file in files:
            if file != '__init__.py' and '.py' == os.path.splitext(file)[1]:
                file_path = os.path.join(dirname, file)
                _ = file_path.split(constant.root_path)[1]
                case_file_list.append(_[1:])

        if files:
            case_file_list.append('')

    return case_file_list

if __name__ == "__main__":
    print(get_case())
    print(get_skip_list())
    # print(get_case_file_list())