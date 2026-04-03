# -*- coding: utf-8 -*-
import logging


def check_word(target):
    def inner(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            logging.info(f"target:{target}, result:{result}")
            if result == target:
                assert True
            else:
                assert False

        return wrapper

    return inner
