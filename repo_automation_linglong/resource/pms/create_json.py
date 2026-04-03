# coding:utf-8
import os
import sys
import json
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from frame import constant

detailed_run_case_file = os.path.join(constant.log_root_path, 'detailed_run_case.txt')


def create_transform_file():
    info = {}
    with open(detailed_run_case_file, 'r', encoding='utf-8') as f:
        text_list = f.readlines()
        for text in text_list:
            text = text.strip()
            print(f"text123:{text}")
            if text:
                try:
                    pms_id = int(text.split('_').pop())
                    info[pms_id] = text
                    print(f"pms_id123:{pms_id}")
                    print(f"dict123:{info[pms_id]}")

                except Exception as e:
                    print(f'{"*" * 10} {e} {"*" * 10}')
                    print(f'{"*" * 10} {text}: 未解析成功 {"*" * 10}')

    with open('id2name.json', 'w') as f:
        print(info)
        json.dump(info, f)

    # with open('name2id.json', 'w') as f:
    #     info2 = {value: key for key, value in info.items()}
    #     json.dump(info2, f)

    # with open('total.txt', 'a', encoding='utf8') as f:
    #     content = f"{datetime.datetime.now()}: {len(info)}\n"
    #     f.write(content)


if __name__ == '__main__':
    path_ = os.path.dirname(os.path.abspath(__file__))
    os.chdir(constant.root_path)
    # os.system('pytest --co script')
    os.chdir(path_)
    create_transform_file()
