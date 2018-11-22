# -*- coding: utf-8 -*-
# @Author  : chenyihui
# @Email   : chenyihui10@126.com
# @Time    :2018-6-25 14:36
"""
decorator for FACTOR_model
author:chenyihui
"""
from functools import wraps
import pandas as pd


def wind_to_df(f):
    @wraps(f)
    def wrap_the_function(*args, **kwargs):
        data = f(*args, **kwargs)
        df = pd.DataFrame(data.Data, index=data.Fields).T
        return df
    return wrap_the_function
