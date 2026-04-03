# -*- coding:utf-8 -*-
import os
import time
import json
import pprint

project_root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
script_dir = os.path.join(project_root_path, 'script')
caselist_file = os.path.join(project_root_path, 'resource', 'caselist.txt')
skip_list_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'skip_list.txt')


def get_skip_list():
    global skip_list_file

    skip_list = []
    with open(skip_list_file, mode='r', encoding='utf8') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('#'):
                continue
            elif line.strip():
                skip_list.append(line.strip())

    return skip_list


def xx(dict_info, _list):
    if _list:
        if dict_info.get(_list[0], None):
            if _list[1:]:
                return xx(dict_info[_list[0]], _list[1:])
            else:
                return dict_info[_list[0]]
        else:
            dict_info[_list[0]] = {}
            if _list[1:]:
                return xx(dict_info[_list[0]], _list[1:])
            else:
                return dict_info[_list[0]]


def get_case_list():
    global project_root_path
    global script_dir
    global caselist_file

    skip_list = get_skip_list()
    case_list = []
    case_dict = {}

    for dirname, subdirs, files in os.walk(script_dir):
        if '__pycache__' in dirname:
            continue

        dirname_list = dirname.split('script')[1].split('/')
        dirname_list[0] = 'script'
        print(dirname_list)

        y = xx(case_dict, dirname_list)

        pprint.pprint(y)
        if files:
            y['files'] = files

    pprint.pprint(case_dict)

    with open('dir.json', 'w', encoding='utf8') as f:
        json.dump(case_dict, f, ensure_ascii=False)


if __name__ == '__main__':
    get_case_list()
