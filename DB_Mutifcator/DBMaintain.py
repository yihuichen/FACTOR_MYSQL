# -*- coding: utf-8 -*-
# @Author  : chenyihui
# @Email   : chenyihui10@126.com
# @Time    :2018-6-25 14:36
"""
daily maintain mfdb in mysql
"""

import sys
from datetime import datetime

from WindPy import w

from DB_Mutifcator.DBManager import ConnectMySQL
from DB_Mutifcator.get_data import DataQuery
from DB_Mutifcator.admin import Admin
from Other_function.some_function import (format_date,
                                          code_convert)


class MaintainMySQL:
    def __init__(self):
        self.connection = ConnectMySQL()
        self.query = DataQuery
    # def history_allA(self, day):  # date shpould be like '20180607'
    #     t = """
    #     return getabkbydate('深证A股;上证A股;中小企业板;创业板',inttodate({}));
    #     """.format(day)
    #     allA_code = TSL.RemoteExecute(t, {})[1]
    #     if len(allA_code) == 0:
    #         print('can not get history allA stockcode')
    #     else:
    #         return allA_code

    def maintain_daily_data(self, day):
        """
        :param day:
        :return: None
        maintain mysql table base_data which is daily updated
        query data from TSL api
        """
        daily_df = self.query(day).get_base_data()
        index_component_df = self.query(day).get_index_component(Admin.main_index_code +
                                                                 Admin.SW_industry_TSL_code_new)
        daily_df.to_sql("base_data",
                        self.connection.engine,
                        if_exists='append',
                        index=False,
                        index_label=None)
        print("insert data into base_data %s" % day)
        index_component_df.to_sql('index_component',
                                  self.connection.engine,
                                  if_exists='append',
                                  index=False,
                                  index_label=None)
        print('insert data into index_component %s' % day)

    def maintain_start_end_data(self, date_need_update=None, day=None):
        """
        :param date_need_update:
        :param day:
        :return: None
        maintain mysql table startST,endST,trade_suspend,trade_resume
        query data from wind api
        """
        if day is None:
            day = datetime.today().strftime("%Y%m%d")
        if date_need_update is None:
            date_need_update = day
        if isinstance(date_need_update, str or datetime):
            date_need_update = [date_need_update]*len(Admin.start_end_update_table)
        elif isinstance(date_need_update, list):
            if len(date_need_update) != len(Admin.start_end_update_table):
                raise ValueError("{0} input should have length {1}".
                                 format(date_need_update, len(Admin.start_end_update_table)))
        else:
            raise TypeError("date_need_update should be type of list or str or datetime not %s"
                            % type(date_need_update))
        for i, table in enumerate(Admin.start_end_update_table):
            data = self.query(day).get_wind_data(table, [date_need_update[i], day])
            if len(data) > 0:
                data.columns = Admin.start_end_dict[table]
                data['stock_code'] = data['stock_code'].apply(code_convert)
                data['date'] = data['date'].apply(format_date)
                data.to_sql(table,
                            self.connection.engine,
                            if_exists='append',
                            index=False,
                            index_label=None)
                print('insert data into table %s' % table)
            else:
                print('no {0} data between {1} and {2}'.
                      format(table, date_need_update[i], day))
        return None

    def maintain_seasonal_data(self, report_period):
        """
        :param report_period:
        :return: None
        maintain mysql table
        profitability,
        solvency,
        capital_structure,
        operational_capability,
        growth_ability,
        cash_flow.
        query data from TSL api
        """
        financial_list = Admin.financial_list
        for financial_type in financial_list:
            financial_data = DataQuery.get_financial_data(report_period, financial_type)
            if len(financial_data) > 0:
                financial_data.to_sql(financial_type,
                                      self.connection.engine,
                                      if_exists='append',
                                      index=False,
                                      index_label=None)
            else:
                print("no {0} data in {1} period"
                      .format(financial_type, report_period))
        return None

    def __del__(self):
        pass


if __name__ == "__main__":
    print('---start---')
    today = datetime.today().strftime("%Y%m%d")
    connect_mysql = ConnectMySQL()
    last_update_date = connect_mysql.get_last_date(Admin.total_table_name[:6])
    daily_last_update = last_update_date[0]
    start_end_last_update = list(map(lambda x: w.tdaysoffset(1, x).Data[0][0], last_update_date[2:]))
    maintain_mysql = MaintainMySQL()
    w.start()
    daily_need_update = w.tdays(daily_last_update, today).Data[0][1:]
    for date in daily_need_update:
        maintain_mysql.maintain_daily_data(date)
        print("update base_data %s" % date)
    maintain_mysql.maintain_start_end_data(start_end_last_update, today)
    print("update startST,endST,trade_suspend,trade_resume done")
