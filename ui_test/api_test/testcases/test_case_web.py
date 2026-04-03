# -*- coding: utf-8 -*-

import pytest
import urllib3
from interface import test_api
from interface import assert_result
from public.log import LOG
import sys
from interface.oper_excel import makedata
data_test = makedata('web')


class Test:
    def setup_class(self):
        LOG.info("测试用例开始执行")

    def teardown_class(self):
        LOG.info('测试用例执行完毕')

    @pytest.mark.web
    @pytest.mark.flaky(reruns=3)
    @pytest.mark.skipif(sys.argv[2] == 'skip', reason="需要跳过web的用例")
    @pytest.mark.parametrize('data', data_test)
    def test_case(self, data):
        """接口测试"""
        urllib3.disable_warnings()
        self.test_case.__func__.__doc__ = data['casename']
        LOG.info('输入参数：用例名:%s,url:%s,参数:%s,请求方式：%s'
                 % (data['casename'], data['url'], data['parms'], data['method']))
        api = test_api.Api(data['url'], data['parms'], data['method'])
        response = api.getJson()
        assert_result.assert_in(data['expect'], response)
