# -*- coding: utf-8 -*-

'''
database_setup, Created on June, 2017
table creation & data initialization
#version: 1.0
'''

# import sys
# sys.path.append(r"C:\Program Files\Tinysoft\Analyse.NET")
# import TSLPy3
from TSL_function.TSL_connect import (TSL,
                                      tsl_frame,
                                      change_code)
import pymysql
from WindPy import w
w.start()
import pandas as pd
from sqlalchemy import create_engine
from DB_Mutifcator.Admin import Admin
from Other_function.some_function import (format_date,
                                          sort_df_columns)
from TSL_function.transcoding import history_allA
from DB_Mutifcator.DB_info import DB_information
from datetime import datetime
class writetoMySQL:
    def __init__(self):
        Admin = Admin()

        # connect MySQL
        self.conn = pymysql.connect(user=Admin.user, passwd=Admin.passwd, host=Admin.host, charset="utf8",
                                    use_unicode=True, port=Admin.port)
        self.cursor = self.conn.cursor()
        # create database
        print('Mysql connected')
        self.cursor.execute(Admin.createDBSQL)
        print('create database')
        self.conn.select_db(Admin.databaseName)
        print("select {} database".format(Admin.databaseName))
        self.cursor.execute(Admin.createSQL_startST)
        print("create table startST")
        self.cursor.execute(Admin.createSQL_endST)
        print("create table endST")
        self.cursor.execute(Admin.createSQL_basedata)
        print("create table basedata")
        engine = create_engine(
            "mysql+pymysql://root:090390704lol@localhost/{}?charset=utf8".format(Admin.databaseName))
        # self.engine = create_engine(
        #     "mysql+mysqldb://{0}:{1}@{2}/{3}?charset=utf8".format(user, passwd, host, databasename))
        start_day = '20180618'
        # today = datetime.today().strftime('%Y%m%d')
        today = '20180621'
        basedata_date = list(map(format_date, w.tdays(start_day, today, "").Data[0]))
        for date in basedata_date:
            stockcode = change_code(history_allA(date))
            stockcode_str = ";".join(stockcode)
            t1 = """
            setsysparam(pn_date(),inttodate({0}));
            setsysparam(pn_rate(),1);
            setsysparam(pn_rateday(),-1);                
            return 
            Query("","{1}",True,"",
            "stock_code",DefaultStockID(),
            "stock_name",CurrentStockName(),
            "high",high(),
            "low",low(),
            "pre_close",StockPrevClose3(),
            "close",close(),
            "open",open(),
            "pct_chg",StockZf3(),
            "turn",StockHsl3(),
            "volume_ratio",volrate(),
            "log_return",StockLnZf3(),
            "is_down",IsDown(),
            "is_up",IsUp(),
            "is_equal",IsEqual(),
            "ZT_one({2})",StockIsZt2(43270),
            "DT_one({3})",StockIsDt2(43270),
            "ZT({4})",StockIsZt(43270),
            "DT({5})",StockIsDt(43270),
            "ever_ZT({6})",StockIsCJZt(43270),
            "ever_DT({7})",StockIsCJDt(43270),            
            "Total_value",StockTotalValue3(),
            "Total_liq_value",StockMarketValue3(),
            "PE_TTM",StockPE3_V(0),
            "PB",StockPNA3_II(),
            "PS",StockPMI3_V(),
            "PC",StockPCF3_V(),
            "PTB",StockPTBR3_II());
            """.format(date, stockcode_str, date, date, date, date, date, date)
            daily_df = tsl_frame(t1)
            # daily_df = change_code(pd.DataFrame(daily_data))
            daily_df['date'] = datetime.strptime(date, '%Y%m%d')
            # substitute columns which accompanied by date
            special_columns = DB_information.base_special_column
            daily_df[special_columns] = daily_df[[i+'(%s)'%date for i in special_columns]]
            for column in special_columns:
                del daily_df[column+'(%s)'%date]
            columns = DB_information.base_data_column
            daily_df = sort_df_columns(daily_df, columns)
            daily_df.to_sql("basedata", engine, if_exists='append', index=False, index_label=None)
            print("insert %s data into basedata" % date)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        print("all done")
    def __del__(self):
        pass


if __name__ == '__main__':
    print('---start---')

    obj = writetoMySQL()

    print('---Done---')
