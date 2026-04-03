# -*- coding:utf-8 -*-
import os
import pprint

ROOTPATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT_DIR = os.path.join(ROOTPATH, 'script')
CASELIST_FILE = os.path.join(ROOTPATH, 'resource', 'caselist.txt')

CASELIST = []
for dirname, subdirs, files in os.walk(SCRIPT_DIR):

    files.sort()

    for file in files:
        if file != '__init__.py' and '.py' == os.path.splitext(file)[1]:
            file_path = os.path.join(dirname, file)
            CASELIST.append(file_path.split(ROOTPATH)[1])

    if files:
        CASELIST.append('')

pprint.pprint(CASELIST)

with open(CASELIST_FILE, mode='w', encoding='utf8') as f:
    for file_path in CASELIST:
        if file_path.strip():
            f.write(file_path + '\n')
