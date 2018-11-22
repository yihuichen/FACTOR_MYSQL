# -*- coding: utf-8 -*-
# @Author  : chenyihui
# @Email   : chenyihui10@126.com
# @Time    :2018-6-25 14:36
"""
create db and table for strategies development
author:chenyihui
"""

from datetime import datetime
import pymysql
from sqlalchemy import create_engine

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
            self.cursor.execute(Admin.createDBSQL)
            print('create database')
            self.conn.select_db(Admin.databaseName)
            print("select {} database".format(Admin.databaseName))
            print("create table startST")
            self.cursor.execute(Admin.createSQL_endST)
            print("create table endST")
            self.cursor.execute(Admin.createSQL_base_data)
            print("create table base_data")
            self.cursor.execute(Admin.createSQL_trade_suspend)
            print("create table trade_suspend")
            self.cursor.execute(Admin.createSQL_trade_resume)
            print("create table trade_resume")
            self.cursor.execute(Admin.createSQL_profitability)
            print("create table profitability")
            self.cursor.execute(Admin.createSQL_solvency)
            print("create table solvency")
            self.cursor.execute(Admin.createSQL_capital_structure)
            print("create table capital_structure")
            self.cursor.execute(Admin.createSQL_operational_capability)
            print("create table operational_capability")
            self.cursor.execute(Admin.createSQL_growth_ability)
            print("create table growth_ability")
            self.cursor.execute(Admin.createSQL_cash_flow)
            print("create table cash_flow")
            self.cursor.execute(Admin.createSQL_report_issue)
            print("create table report_issue")
            self.cursor.execute(Admin.createSQL_performance_forecast)
            print("create table performance_forecast")
            self.cursor.execute(Admin.createSQL_performance_fast_report)
            print("create table performance_fast_report")
            self.cursor.execute(Admin.createSQL_index_component)
            print("create table index_component")
            engine = create_engine(
                "mysql+pymysql://root:admin@localhost/{}?charset=utf8".format(Admin.databaseName))
            start_day = '20180630'
            today = '20180716'
            base_data_date = list(map(format_date, w.tdays(start_day, today, "").Data[0]))
            for date in base_data_date:
                tsl_data = DataQuery(date)
                daily_df = tsl_data.get_base_data()
                if int(date) < 20140221:
                    index_component_df = tsl_data.get_index_component(Admin.main_index_code +
                                                                      Admin.SW_industry_TSL_code_old)
                else:
                    index_component_df = tsl_data.get_index_component(Admin.main_index_code +
                                                                      Admin.SW_industry_TSL_code_new)
                daily_df.to_sql("base_data",
                                engine,
                                if_exists='append',
                                index=False,
                                index_label=None)
                print("insert %s data into base_data" % date)
                index_component_df.to_sql("index_component",
                                          engine,
                                          if_exists='append',
                                          index=False,
                                          index_label=None)
                print("insert %s data into table index_component" % date)
            start_day = '20100105'
            wind_data = DataQuery('20180620')
            special_treated_start = wind_data.get_wind_data('startST', [start_day, today])
            special_treated_end = wind_data.get_wind_data('endST', [start_day, today])
            suspend_data = wind_data.get_wind_data('suspend', [start_day, today])
            resume_data = wind_data.get_wind_data('resume', [start_day, today])
            if len(special_treated_start) > 0:
                special_treated_start.columns = Admin.startST_column
                special_treated_start['stock_code'] = special_treated_start['stock_code'].apply(code_convert)
                special_treated_start['date'] = special_treated_start['date'].apply(format_date)
                special_treated_start.to_sql("startST",
                                             engine,
                                             if_exists='append',
                                             index=False,
                                             index_label=None)
                print('insert data into table startST between {0} and {1}'.
                      format(start_day, today))
            else:
                print('no startST data between {0} and {1}'.format(start_day, today))
            if len(special_treated_end) > 0:
                special_treated_end.columns = Admin.endST_column
                special_treated_end['stock_code'] = special_treated_end['stock_code'].apply(code_convert)
                special_treated_end['date'] = special_treated_end['date'].apply(format_date)
                special_treated_end.to_sql("endST",
                                           engine,
                                           if_exists='append',
                                           index=False,
                                           index_label=None)
                print('insert data into table endST between {0} and {1}'
                      .format(start_day, today))
            else:
                print('no endST data between {0} and {1}'.format(start_day, today))
            if len(suspend_data) > 0:
                suspend_data.columns = Admin.trade_suspend_column
                suspend_data['stock_code'] = suspend_data['stock_code'].apply(code_convert)
                suspend_data['date'] = suspend_data['date'].apply(format_date)
                suspend_data.to_sql("trade_suspend",
                                    engine,
                                    if_exists='append',
                                    index=False,
                                    index_label=None)
                print('insert data into table trade_suspend between {0} and {1}'
                      .format(start_day, today))
            else:
                print('no suspend_data between {0} and {1}'.format(start_day, today))
            if len(resume_data) > 0:
                resume_data.columns = Admin.trade_resume_column
                resume_data['stock_code'] = resume_data['stock_code'].apply(code_convert)
                resume_data['date'] = resume_data['date'].apply(format_date)
                resume_data.to_sql("trade_resume",
                                   engine,
                                   if_exists='append',
                                   index=False,
                                   index_label=None)
                print('insert data into table trade_resume between {0} and {1}'
                      .format(start_day, today))
            else:
                print('no resume_data between {0} and {1}'.format(start_day, today))
            # ----start build financial table-----------------------------------
            from functools import reduce
            report_period = reduce(lambda x, y: x + y,
                                   [
                                    [str(i) + '0331', str(i) + '0630', str(i) + '0930', str(i) + '1231']
                                    for i in range(2007, 2018)
                                   ]
                                   )
            financial_list = Admin.financial_list
            for period in report_period:
                for financial_type in financial_list:
                    financial_data = DataQuery.get_financial_data(period, financial_type)
                    financial_data.to_sql(financial_type,
                                          engine,
                                          if_exists='append',
                                          index=False,
                                          index_label=None)
                    print("insert data into table {0} of {1}".format(financial_type, period))
            # DataQuery.get_component_data()
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
    print('---start---')
    obj = WriteToMySQL()
    print('---Done---')
