# -*- coding:utf-8 -*-
import os

project_root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
script_dir = os.path.join(project_root_path, 'script', 'dbus', 'sessionBus', 'inputDeviceTouchPad')

for dir_name, subdir, files in os.walk(script_dir):
    if '__pycache__' in dir_name:
        continue

    files.sort()
    for file in files:
        print(file)
    else:
        print('+' * 50)
