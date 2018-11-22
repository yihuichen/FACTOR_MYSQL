# -*- coding: utf-8 -*-
# @Author  : chenyihui
# @Email   : chenyihui10@126.com
# @Time    :2018-6-25 14:36
import pandas as pd
import sys

sys.path.append(r"C:\Program Files\Tinysoft\Analyse.NET")

import TSLPy3 as TSL

TSL.ConnectServer("tsl.tinysoft.com.cn", 443)
dl = TSL.LoginServer("swtzb", "swtzb888888")


def change_code(df, option=None):
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
        if option is None:
            for column in columns:
                if isinstance(df[column][0], bytes):
                    df[column] = list(map(f, list(df[column])))
        else:
            df = df.applymap(f)
    elif isinstance(df, bytes):
        df = f(df)
    else:
        raise TypeError("Invalid argument the param input should be bytes,list,DataFrame"
                        "not %s" % type(df))
    return df


def change_code_all_df(df):
    def f(x):
        if isinstance(x, bytes):
            x = str(x, 'GBK')
        else:
            x = x
        return x
    df = df.applymap(f)
    return df


def tsl_frame(t1):
    data = TSL.RemoteExecute(t1, {})
    if data[0] == -1:
        print("wrong TSL statement or syntax error")
    elif data[0] == 0:
        result = pd.DataFrame(data[1])
        return result


def history_allA(date):  # date shpould be like '20180607'
    t = """
    return getabkbydate('深证A股;上证A股;中小企业板;创业板',inttodate({})); 
    """.format(date)
    all_code = TSL.RemoteExecute(t, {})[1]
    if len(all_code) == 0:
        print('can not get history allA stockcode')
    else:
        return all_code


if dl[0] == 0:
    __all__ = ['TSL', 'tsl_frame', 'history_allA', 'change_code']
else:
    __all__ = ['change_code']
    print("can not connect to TSL")

