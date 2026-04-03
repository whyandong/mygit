# -*- coding: utf-8 -*-

import pytest
import os
from public.log import LOG
import sys
from interface.oper_excel import makedata
from interface.oper_cmd import select_file

data_test = makedata('system')


class Test:
    def setup_class(self):
        LOG.info("测试用例开始执行")

    def teardown_class(self):
        LOG.info('测试用例执行完毕')

    @pytest.mark.system
    @pytest.mark.flaky(reruns=1)
    @pytest.mark.skipif(sys.argv[2] == 'skip', reason="需要跳过的测试用例")
    @pytest.mark.parametrize('data', [data_test[6]])
    def test_check_system_os_release(self, data):
        """系统信息-os-release文件"""
        self.test_check_system_os_release.__func__.__doc__ = data['casename']
        LOG.info('输入参数：用例名:%s,参数:%s,期望：%s' % (
            data['casename'],
            data['parms'],
            data['expect'],
        ))
        response = select_file(self.test_check_system_os_release.__name__, data['parms'],data['expect'])
        assert set(response) == {'passed'}