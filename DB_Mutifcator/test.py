# -*- coding: utf-8 -*-
# import sys
# sys.path.append(r"C:\Program Files\Tinysoft\Analyse.NET")
import TSLPy3
from TSL_function.transcoding import change_code
from Other_function.some_function import format_date
from datetime import datetime
from WindPy import w
import pandas as pd
w.start()

def history_allA(date):    #date should be like '20180607'
    t = """
    return getabkbydate('深证A股;上证A股;中小企业板;创业板',inttodate({})); 
    """.format(date)
    allA_code = TSLPy3.RemoteExecute(t, {})[1]
    if len(allA_code) == 0:
        print('can not get history allA stockcode')
    else:
        return allA_code

# 获取交易日与固定报告期
start_day = '20070101'
today = datetime.today().format('%Y%m%d')
basedata_date = list(map(format_date, w.tdays(start_day, today, "").Data[0]))
for date in basedata_date:
    stockcode = history_allA(date)
    stockcode_str = ";".join(stockcode)
    t1 = """
    setsysparam(pn_date(),inttodate({0}));
    return 
    Query("A股","",True,"",
    "stockcode",DefaultStockID(),
    "stockname",CurrentStockName(),
    "high",high(),
    "low",low(),
    "preclose",StockPrevClose3(),
    "close",close(),
    "open",open(),
    "pct_chg",StockZf3(),
    "turn",StockHsl3(),
    "volumeratio",volrate(),
    "logreturn",StockLnZf3(),
    "isdown",IsDown(),
    "isup",IsUp(),
    "isequal",IsEqual(),
    "ZT_one({1})",StockIsZt2(42466),
    "DT_one({2})",StockIsDt2(42437),
    "ZT({3})",StockIsZt(38450),
    "DT({4})",StockIsDt(38450),
    "CJZT({5})",StockIsCJZt(38450),
    "CJDT({6})",StockIsCJDt(38450),
    "Totalvalue",StockTotalValue3(),
    "Totalliqvalue",StockMarketValue3(),
    "PETTM",StockPE3_V(0),
    "PB",StockPNA3_II());
    """.format(date, date, date, date, date, date, date)


from functools import reduce
report_period = reduce(lambda x, y:x+y, [[str(i)+'0331', str(i)+'0630', str(i)+'0930', str(i)+'1231'] for i in range(2007,2018)])


date = '20080426'
t1 = """
setsysparam(pn_date(),inttodate({0}));
return 
Query("A股","",True,"","代码",DefaultStockID(),
"名称",CurrentStockName(),
"最高价",high(),
"最低价",low(),
"昨收",StockPrevClose3(),
"收盘价",close(),
"开盘价",open(),
"涨幅(%)",StockZf3(),
"换手率(%)",StockHsl3(),
"量比",volrate(),
"对数收益率(%)",StockLnZf3(),
"是否下跌",IsDown(),
"是否上涨",IsUp(),
"是否平盘",IsEqual(),
"指定日是否一字涨停({1})",StockIsZt2(42466),
"指定日是否一字跌停({2})",StockIsDt2(42437),
"是否涨停({3})",StockIsZt(38450),
"是否跌停({4})",StockIsDt(38450),
"是否曾经涨停({5})",StockIsCJZt(38450),
"是否曾经跌停({6})",StockIsCJDt(38450),
"最新总市值(万)",StockTotalValue3(),
"最新流通市值(万)",StockMarketValue3(),
"市盈率(最近12个月)(类型=0)",StockPE3_V(0),
"市盈率(专用)(类型=0)",StockPE3_IV(0),
"市净率(最新财务数据)",StockPNA3_II());
""".format(date, date, date, date, date, date, date)
d2 = TSLPy3.RemoteExecute(t1, {})[1]
df5 = change_code(pd.DataFrame(d2))
