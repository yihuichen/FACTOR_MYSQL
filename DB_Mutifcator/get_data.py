# -*- coding: utf-8 -*-
# @Author  : chenyihui
# @Email   : chenyihui10@126.com
# @Time    :2018-6-25 14:36
"""
get data needed to insert into mysql
data from TSL api and Wind api
"""
from datetime import datetime
import pandas as pd

from WindPy import w

from TSL_function.TSL_connect import (TSL,
                                      tsl_frame,
                                      change_code,
                                      history_allA)
from DB_Mutifcator.admin import Admin
from Other_function.some_function import (format_date,
                                          sort_df_columns,
                                          code_convert)

from Other_function.date_function import date_to_num
from My_decorator import wind_to_df

w.start()


class DataQuery:
    def __init__(self, date):
        self.date = date

    def get_base_data(self):
        """
        :return: base_data which is a DataFrame()
        query all A stock base data such as
                 open close high low
                 and so on
        by TSL api
        """
        num = date_to_num(self.date)
        stock_code = change_code(history_allA(self.date))
        stock_code_str = ";".join(stock_code)
        t1 = Admin.base_data_statement.format(self.date, stock_code_str, num)
        daily_df = change_code(tsl_frame(t1))
        # daily_df = change_code(pd.DataFrame(daily_data))
        # daily_df['date'] = datetime.strptime(self.date, '%Y%m%d')
        daily_df['date'] = self.date
        columns = Admin.base_data_column
        daily_df = sort_df_columns(daily_df, columns)
        daily_df = daily_df.replace([float("inf"), float("-inf")], 100000000)
        return daily_df

    @wind_to_df
    def get_wind_data(self, field, start_end=None):
        # start_end = args
        if field is None:
            print("Invalid argument!")
        if start_end is None:
            data = w.wset(Admin.wind_fields[field], "startdate={0};enddate={1}"
                          .format(self.date, self.date))
        elif len(start_end) == 2:
            data = w.wset(Admin.wind_fields[field], "startdate={0};enddate={1}"
                          .format(start_end[0], start_end[1]))
        else:
            print("the length of param should be 2")
        return data

    @staticmethod
    def get_financial_data(report_period=None, financial_type=None):
        """
        :param report_period:
        :param financial_type:
        :return: a financial DataFrame() data
        report_period should be str(year)+'0331' or '0630' or '0930' or '1231'
        financial_type should be one of
                   profitability
                   solvency
                   capital_structure
                   operational_capability
                   growth_ability
                   cash_flow
        query financial data by TSL api
        """
        if(report_period is None) or (financial_type is None):
            print("Invalid arguments!")
        stock_code = change_code(history_allA(report_period))
        stock_code_str = ";".join(stock_code)
        tsl_statement = Admin.financial_dict[financial_type].format(stock_code_str, report_period)
        financial_df = tsl_frame(tsl_statement)
        financial_df = change_code(financial_df, option=1 if financial_type == "performance_forecast" else None)
        # financial_df['report_period'] = datetime.strptime(report_period, '%Y%m%d')
        financial_df['report_period'] = report_period
        columns = Admin.financial_column_dict[financial_type]
        financial_df = sort_df_columns(financial_df, columns)
        financial_df = financial_df.replace([float("inf"), float("-inf")], 100000000)
        return financial_df

    @staticmethod
    def get_component_data(index_code, component_update_date):
        """
        :param index_code:
        :param component_update_date:
        :return: component of index such as 300
        return a dataframe
        """
        if isinstance(component_update_date, str or datetime):
            data = w.wset("sectorconstituent", "date={0};windcode={1}".
                          format(component_update_date, index_code))
            data_df = pd.DataFrame(data.Data, index=data.Fields).T
            return data_df
        elif isinstance(component_update_date, list):
            df = pd.DataFrame()
            for date in component_update_date:
                data = w.wset("sectorconstituent", "date={0};windcode={1}".format(date, index_code))
                data_df = pd.DataFrame(data.Data, index=data.Fields).T
                df = df.append(data_df)
            return df
        else:
            raise TypeError("component_update_date should be "
                            "str or datetime or list not %s" % type(component_update_date))

    def get_index_component(self, index_code, day=None):
        used_date = self.date if day is None else day
        if isinstance(index_code, str):
            tsl_statement = Admin.index_component_statement.format(index_code, used_date)
            df = change_code(tsl_frame(tsl_statement))
            df[Admin.index_component_column[1]] = df[Admin.index_component_column[0]]
            df_new = df[Admin.index_component_column[1]]
            return df_new
        elif isinstance(index_code, list):
            df_total = pd.DataFrame()
            for index in index_code:
                tsl_statement = Admin.index_component_statement.format(index, used_date)
                df = change_code(tsl_frame(tsl_statement))
                df[Admin.index_component_column[1]] = df[Admin.index_component_column[0]]
                df_new = df[Admin.index_component_column[1]]
                df_total = df_total.append(df_new)
            return df_total
        else:
            raise TypeError("index_code should be str or list not%s" % type(index_code))


if __name__ == '__main__':
    A = DataQuery('20100105')
    # wind_data = A.get_wind_data('resume', start_end=None)
    # wind_data['wind_code'] = wind_data['wind_code'].apply(code_convert)
    # TSL_data = A.get_base_data()
    # index_code = Admin.SW_industry_TSL_code_old
    # for code in index_code:
    #     try:
    #         index_data = A.get_index_component(code)
    #         print(code)
    #     except:
    #         continue
    A.get_wind_data('suspend', start_end=['20100105', '20130105'])
    # index_data = A.get_index_component(Admin.main_index_code + Admin.SW_industry_TSL_code)
    # wind_data = A.get_wind_data('startST')
    # wind_Data = A.get_wind_data('suspend', start_end=['20180621', '20180629'])
    # print(wind_Data.ix[641, 'suspend_reason'])
    # print(wind_Data['suspend_reason'])
    # data_ = A.get_financial_data(report_period='20171231', financial_type="performance_forecast")
    # stock_code = change_code(history_allA('20171231'))
    # stock_code_str = ";".join(stock_code)
    # tsl_statement = Admin.financial_dict["operational_capability"].format(stock_code_str, '20171231')
    # financial_df = tsl_frame(tsl_statement)
    # financial_df = financial_df.replace(float("inf"), 10000000)
    # print(wind_data)

