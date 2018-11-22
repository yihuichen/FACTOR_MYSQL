# -*- coding: utf-8 -*-
# @Author  : chenyihui
# @Email   : chenyihui10@126.com
# @Time    :2018-7-17 14:15
"""
使用wind api将停牌复牌数据取出，导入数据库中，
由于wind api取停牌复牌数据每次访问只能提取一个月的，所以逐月提取，插入数据库。
值得注意的是，
"""
import pymysql
from sqlalchemy import create_engine
import pandas as pd

from WindPy import w

from DB_Mutifcator.admin import Admin
from Other_function.some_function import (format_date,
                                          code_convert)
from DB_Mutifcator.get_data import DataQuery

w.start()


class WriteToMySQL:
    def __init__(self):
        self.conn = pymysql.connect(user=Admin.user,
                                    passwd=Admin.passwd,
                                    host=Admin.host,
                                    charset="utf8",
                                    use_unicode=True,
                                    port=Admin.port)
        self.cursor = self.conn.cursor()
        print('Mysql connected')
        # self.cursor.execute("set autocommit = 0")
        # print("autocommit closed")
        try:
            self.conn.select_db(Admin.databaseName)
            print("select {} database".format(Admin.databaseName))
            engine = create_engine(
                "mysql+pymysql://root:admin@localhost/{}?charset=utf8".format(Admin.databaseName))
            start_day = '20100116'
            today = '20100716'
            # base_data_date = list(map(format_date, w.tdays(start_day, today, "").Data[0]))
            wind_data = DataQuery('20180620')
            suspend_df, resume_df = pd.DataFrame(), pd.DataFrame()
            while int(start_day) < int(today):
                end_day = format_date(w.tdaysoffset(1, start_day, "Days=Alldays;Period=M").Data[0][0])
                suspend_data = wind_data.get_wind_data('suspend', [start_day, end_day])
                resume_data = wind_data.get_wind_data('resume', [start_day, end_day])
                start_day = end_day
                if len(suspend_data) > 0:
                    suspend_df = suspend_df.append(suspend_data)
                if len(resume_data) > 0:
                    resume_df = resume_df.append(suspend_data)
            suspend_df = suspend_df.drop_duplicates()
            resume_df = resume_df.drop_duplicates()
            suspend_df.columns = Admin.trade_suspend_column
            suspend_df['stock_code'] = suspend_df['stock_code'].apply(code_convert)
            suspend_df['date'] = suspend_df['date'].apply(format_date)
            suspend_data.to_sql("trade_suspend",
                                engine,
                                if_exists='append',
                                index=False,
                                index_label=None)
            print('insert data into table trade_suspend between {0} and {1}'
                  .format(start_day, today))
            resume_df.columns = Admin.trade_resume_column
            resume_df['stock_code'] = resume_df['stock_code'].apply(code_convert)
            resume_df['date'] = resume_df['date'].apply(format_date)
            resume_df.to_sql("trade_resume",
                             engine,
                             if_exists='append',
                             index=False,
                             index_label=None)
            print('insert data into table trade_resume between {0} and {1}'
                  .format(start_day, today))
            print("all data insert done")

        except pymysql.Error as e:
            # self.conn.rollback()
            # print("roll back")
            print("Error {0}: {1}".format(e.args[0], e.args[1]))

        finally:
            self.conn.commit()
            print("commit done")
            self.cursor.close()
            print("cursor close")
            self.conn.close()
            print("connection close")

    # Release
    def __del__(self):
        pass


if __name__ == '__main__':
    A = WriteToMySQL()
