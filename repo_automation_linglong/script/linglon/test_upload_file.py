import allure
import pytest
from frame.constant import upload_file
from frame.projectLog import log

import requests
import time
from frame.read_json import post_read_json

from frame.get_login import get_login
from frame.read_config import get_values_from_config

logger = log()

class Test_linglong:


    @pytest.mark.parametrize('expected,url,headers,data,casename', post_read_json(upload_file))
    def test_task_list(self,expected,url,headers,data,casename):

        path_url = get_values_from_config(cmd='linglong',key='qliyun')
        progreess_path = path_url + url
        #headers['X-Token'] = get_login()
        headers = {"Content-type" : "multipart/form-data"}

        file_url = "/home/zhanyuanyuan/Downloads/com.51ifind_1.10.12.377_x86_64.uab"

        result = requests.post(url=progreess_path,file=file_url,headers=headers,data=data).json()
        print(result)
        result_code = result['code']
        assert result_code == expected

        logger.info("%s 用例执行通过" % casename)


if __name__ == '__main__':
    pytest.main(['-s', 'test_upload_file.py'])