# -*- coding:utf-8 -*-
import os
import pprint

project_root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
script_dir = os.path.join(project_root_path, 'script')
caselist_file = os.path.join(project_root_path, 'resource', 'caselist.txt')


def get_case_list():
    global project_root_path
    global script_dir
    global caselist_file

    case_list = []
    for dirname, subdirs, files in os.walk(script_dir):

        files.sort()

        for file in files:
            if file != '__init__.py' and '.py' == os.path.splitext(file)[1]:
                file_path = os.path.join(dirname, file)
                _ = file_path.split(project_root_path)[1]
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
