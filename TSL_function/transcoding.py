# -*- coding: utf-8 -*-
# author: chen_yi_hui

import pandas as pd

import TSLPy3


def change_code(df):
    # 处理天软得到的编码问题
    def f(x):
        if isinstance(x, bytes):
            x = str(x, 'GBK')
        else:
            x = x
        return x
    if isinstance(df, list):
        df = list(map(f, df))
    elif isinstance(df, pd.DataFrame):
        columns = list(map(f, list(df.columns)))
        df.columns = columns
        for column in columns:
            if isinstance(df[column][0], bytes):
                df[column] = list(map(f, list(df[column])))
    elif isinstance(df, bytes):
        df = f(df)
    else:
        raise TypeError("Invalid argument the param input should be bytes,list,DataFrame"
                        "not %s" % type(df))
    return df


def history_allA(date):  # date shpould be like '20180607'
    t = """
    return getabkbydate('深证A股;上证A股;中小企业板;创业板',inttodate({})); 
    """.format(date)
    allA_code = TSLPy3.RemoteExecute(t, {})[1]
    if len(allA_code) == 0:
        print('can not get history allA stockcode')
    else:
        return allA_code