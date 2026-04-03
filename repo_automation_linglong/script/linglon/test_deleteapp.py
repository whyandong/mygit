import allure
import pytest
from frame.constant import deleteapp
from frame.projectLog import log

import requests
import time
from frame.read_json import post_read_json

from frame.get_login import get_login
from frame.read_config import get_values_from_config

logger = log()

class Test_linglong:


    @pytest.mark.parametrize('expected,url,headers,data,casename', post_read_json(deleteapp))
    def test_task_list(self,expected,url,headers,data,casename):

        path_url = get_values_from_config(cmd='linglong',key='qliyun')
        progreess_path = path_url + url
        headers['X-Token'] = get_login()
        result = requests.post(url=progreess_path,headers=headers,data=data).json()
        print(result)
        result_code = result['code']
        assert result_code == expected

        logger.info("%s 用例执行通过" % casename)


if __name__ == '__main__':
    pytest.main(['-s', 'test_deleteapp.py'])