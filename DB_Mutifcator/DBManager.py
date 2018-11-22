# -*- coding: utf-8 -*-
# @Author  : chenyihui
# @Email   : chenyihui10@126.com
# @Time    :2018-6-25 14:36

'''
database_setup, Created on Jun, 2017
#version: 1.0
DB Manager
'''
import sys
import pandas as pd
from sqlalchemy import *

from DB_Mutifcator.admin import Admin


class ConnectMySQL:
    def __init__(self,
                 user=Admin.user,
                 passwd=Admin.passwd,
                 host=Admin.host,
                 databasename=Admin.databaseName):
        try:
            # connect MySQL
            self.engine = create_engine(
                "mysql+pymysql://{0}:{1}@{2}/{3}?charset=utf8".format(user, passwd, host, databasename))
        except:
            info = sys.exc_info()
            print(info[0], ":", info[1])

    # number_list:backward period///forward output!!!
    def update_value(self, table_name, field, value, condition):
        str_sql = 'UPDATE {0} SET {1} = {2} where {3}'.format(table_name, field, value, condition)
        self.engine.execute(str_sql)

    def drop_table(self, table_name):
        str_sql = 'DROP TABLE %s' % table_name
        self.engine.execute(str_sql)
        print("drop table %s" % table_name)

    def select_value(self, table_name_list, number_list, symbol):
        if len(table_name_list) != len(number_list):
            print("input error")
            return "input error"
        else:
            result = []
            for i in range(len(table_name_list)):
                print("select from table {}".format(table_name_list[i]))
                str_sql = "select * from " + str(table_name_list[i]) + " where stkcd='" + str(
                    symbol) + "' order by ntime DESC limit " + str(number_list[i])
                result.append(pd.read_sql(str_sql, self.engine))
            print("select done")
            return result

    # All data:normal backward output
    def select_all_value(self, table_name, symbol):
        str_sql = "select * from {0} where stkcd='{1}'".format(table_name, symbol)
        result = pd.read_sql(str_sql, self.engine)
        print("select done")
        return result

    def insert_value(self, table_name_list, data_list):
        if len(table_name_list) != len(data_list):
            print("input error")
        else:
            for i in range(len(table_name_list)):
                data_list[i].to_sql(table_name_list[i], self.engine, if_exists='append', index=False, index_label=None)
                print("insert data into {}".format(table_name_list[i]))

    def delete_data(self, table_name, symbol):
        str_sql = "delete from {0} where stkcd='{1}'".format(table_name, symbol)
        self.engine.execute(str_sql)
        print("delete {} data from table {}".format(symbol, table_name))

    def get_engine(self):
        return self.engine

    def get_last_date(self, table_name=None):
        if table_name is None:
            print("Invalid argument")
        if isinstance(table_name, str):
            if table_name in Admin.table_name:
                try:
                    sql_date = 'select date from %s order by date desc limit 1' % table_name
                except:
                    sql_date = 'select report_period from %s order by report_period desc limit 1' % table_name
                return list(self.engine.execute(sql_date))[0][0][:10]
            else:
                raise ValueError("no table named %s" % table_name)
        elif isinstance(table_name, list):
            sql_date_list = []
            for table_ in table_name:
                if table_name in Admin.table_name:
                    try:
                        sql_date = 'select date from %s order by date desc limit 1' % table_
                    except:
                        sql_date = 'select report_period from %s order by report_period desc limit 1' % table_name
                    sql_date_list.append(list(self.engine.execute(sql_date))[0][0][:10])
                else:
                    raise ValueError("no table named %s" % table_)
            return sql_date_list
        else:
            raise TypeError('table_name input should be str or list but {} received' % type(table_name))

    def sql_user_verify(self, user_id, password):
        str_sql = 'select password,type from userinfo where userid ="{}"'.format(str(user_id))
        result = list(self.engine.execute(str_sql))
        if not result:
            print("No user")
            return -1
        else:
            pwd = result[0][0]
            type_ = result[0][1]
            if pwd != str(password):
                print("password not correct")
                return 0
            else:
                return type_

    def __del__(self):
        # disconnect
        self.engine.dispose()


if __name__ == '__main__':
    print('---start---')

    obj = ConnectMySQL()
    a = obj.sqluser_verify("200047", "123456")
    # print obj.get_last_date()
    print(a)
    print('---Done---')
