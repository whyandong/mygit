# coding:utf-8
import os
import json
import argparse

file_dir_path = os.path.dirname(os.path.abspath(__file__))  # 文件所在路径
root_path = os.path.dirname(file_dir_path)  # 文件所在路径

parser = argparse.ArgumentParser()
parser.add_argument('result_file_path')
args = parser.parse_args()


def get_result(result_file_path):
    with open(result_file_path, 'r') as f:
        info = json.load(f)

    result_dict = {"pass": 0, "fail": 0, "blocked": 0}

    for item in info:
        res = info[item]["result"]
        result_dict[res] += 1

    print(json.dumps(result_dict))


if __name__ == "__main__":
    os.chdir(root_path)
    get_result(args.result_file_path)
