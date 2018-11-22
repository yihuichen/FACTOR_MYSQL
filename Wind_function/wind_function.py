# -*- coding: utf-8 -*-
# @Author  : chenyihui
# @Email   : chenyihui10@126.com
# @Time    :2018-7-2 10:31

from WindPy import w

from TSL_function.TSL_connect import (history_allA,
                                      change_code)
from Other_function.some_function import code_convert

w.start()


def get_sw_industry(code_list, date):
    """
    :param code_list:
    :param date:
    :return: sw level one industry
    date should be trade date
    code_list can not duplicated
    """
    if len(set(code_list)) != len(code_list):
        raise ValueError("duplicated value in code_list input")
    else:
        sw_industry_code = w.wsd(code_list, "indexcode_sw", date, date, "industryType=1").Data[0]
    return sw_industry_code


if __name__ == '__main__':
    stock_code = code_convert(change_code(history_allA('20180627')))
    industry_code = get_sw_industry(stock_code, '20180627')

