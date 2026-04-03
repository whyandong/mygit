# -*- coding:utf-8 -*-
import os
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
                _ = line.strip()
                if _.startswith('/'):
                    skip_list.append(_[1:])
                else:
                    skip_list.append(_)

    return skip_list


def get_case_list():
    global project_root_path
    global script_dir
    global caselist_file

    skip_list = get_skip_list()
    case_list = []
    for dirname, subdirs, files in os.walk(script_dir):

        files.sort()

        for file in files:
            if file != '__init__.py' and '.py' == os.path.splitext(file)[1]:
                file_path = os.path.join(dirname, file)
                _ = file_path.split(project_root_path)[1]
                if _[1:] not in skip_list:
                    case_list.append(_[1:])

        if files:
            case_list.append('')

    pprint.pprint(case_list)

    with open(caselist_file, mode='w', encoding='utf8') as f:
        for file_path in case_list:
            if file_path.strip():
                f.write(file_path + '\n')


if __name__ == '__main__':
    get_case_list()
