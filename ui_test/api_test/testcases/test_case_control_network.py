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
    @pytest.mark.parametrize('data', [data_test[11]])
    def test_control_network(self, data):
        """有线网络-打开关闭网络"""
        self.test_control_network.__func__.__doc__ = data['casename']
        LOG.info('输入参数：用例名:%s,参数:%s' % (
            data['casename'],
            data['parms'],
        ))
        response = select_file(self.test_control_network.__name__, data['parms'],data['expect'])
        assert set(response) == {'passed'}