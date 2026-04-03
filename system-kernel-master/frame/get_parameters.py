# -*- coding: utf-8 -*-
import json
import os
import logging

from frame import constant


def get_build_parameters():
    task_id = os.environ["TASK_ID"]
    product_id = os.environ["PRODUCT_ID"]
    user_name = os.environ["UserName"]
    logging.info(f'task_id:{task_id}')
    logging.info(f'product_id:{product_id}')
    logging.info(f'user_name:{user_name}')

    with open(os.path.join(constant.root_path, 'resource', 'pms', 'pms_job.json'), "r") as f:
        json_data = json.load(f)
        json_data["task_id"] = task_id
        json_data["product_id"] = product_id
        json_data["user_name"] = user_name
        json_new_data = json.dumps(dict(json_data), ensure_ascii=False)

        with open(os.path.join(constant.root_path, 'resource', 'pms', 'pms_job.json'), "w") as f1:
            f1.write(json_new_data)
