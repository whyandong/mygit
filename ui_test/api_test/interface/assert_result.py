# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.getcwd())

from interface.analysis_dict import res
from public.log import LOG, logger


@logger('断言测试结果')
def assert_in(expect, response):
    if len(expect.split('=')) > 1:
        data = expect.split('&')
        result = dict([(item.split('=')) for item in data])
        response_value = ([(str(res(response, key))) for key in result.keys()])
        expect_value = ([(str(value)) for value in result.values()])
        assert response_value == expect_value
    else:
        LOG.warn('填写测试预期值')
        return {"code": 2, 'result': '填写测试预期值'}


@logger('断言测试结果')
def assertre(expect):
    if len(expect.split('=')) > 1:
        data = expect.split('&')
        result = dict([(item.split('=')) for item in data])
        return result
    else:
        LOG.warn('填写测试预期值')
        raise {"code": 1, 'result': '填写测试预期值'}

