# -*- coding: utf-8 -*-
# @Author  : chenyihui
# @Email   : chenyihui10@126.com
# @Time    :2018-6-25 14:36
"""
FACTOR_model MYSQL db information
such as create table statement,table name, table column, TSL statement
author: chenyihui
"""


def get_sql_statement(table_name, table_column):
    """
    :param table_name:
    :param table_column:
    :return: sql_statement
    to create financial table SQL statement using a function
    """
    begin_statement = 'create table if not exists %s(\
                        stock_code char(10) NOT NULL, \
                        stock_name char(10) NOT NULL,' % table_name
    end_statement = ',report_period date,\
                    primary key(stock_code, report_period));'
    between_statement = ",".join([column + ' float(18,4)' for column in table_column[2:-1]])
    sql_statement = begin_statement + between_statement + end_statement
    return sql_statement


class Admin:
    databaseName = 'mfdb'
    user = 'root'
    passwd = 'admin'
    host = 'localhost'
    port = 3306

    total_table_name = ['base_data',
                        'index_component',
                        'startST',
                        "endST",
                        "trade_suspend",
                        "trade_resume",
                        "profitability",
                        "solvency",
                        "capital_structure",
                        "operational_capability",
                        "growth_ability",
                        "cash_flow",
                        'report_issue',
                        'performance_forecast',
                        'performance_fast_report']

    daily_update_table = ['base_data']

    start_end_update_table = ['startST',
                              "endST",
                              "trade_suspend",
                              "trade_resume"]

    seasonal_update_table = ["profitability",
                             "solvency",
                             "capital_structure",
                             "operational_capability",
                             "growth_ability",
                             "cash_flow"]

    # SQL statements
    createDBSQL = 'create database if not exists ' + databaseName

    # ------------- stock pricing user_information tables -------------
    createSQL_userInfo = 'create table if not exists userinfo( \
                            userid char(10) NOT NULL,\
                            name char(64),\
                            password char(20),\
                            type char(10),\
                            primary key(userid)\
                            );'

    # ------------- stock pricing update date tables -------------
    createSQL_date = 'create table if not exists date(\
                                date varchar(20) NOT NULL,\
                                primary key(date)\
                                );'
    # ------------- create base_data table -------------

    createSQL_base_data = 'create table if not exists base_data(\
                            stock_code char(10) NOT NULL,\
                            stock_name char(10) NOT NULL,\
                            high float(18,4),\
                            low float(18,4),\
                            pre_close float(18,4),\
                            close float(18,4),\
                            open float(18,4),\
                            pct_chg float(18,4),\
                            turn float(18,4),\
                            volume_ratio float(18,4),\
                            log_return float(18,4),\
                            is_down int,\
                            is_up int,\
                            is_equal int,\
                            ZT_one int,\
                            DT_one int,\
                            ZT int,\
                            DT int,\
                            ever_ZT int,\
                            ever_DT int,\
                            Total_value float(18,4),\
                            Total_liq_value float(18,4),\
                            PE_TTM float(18,4),\
                            PB float(18,4),\
                            PS float(18,4),\
                            PC float(18,4),\
                            PTB float(18,4),\
                            date date NOT NULL,\
                            issue_date date NOT NULL,\
                            primary key(stock_code,date)\
                            );'

    base_data_statement = """
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
        "ZT_one",StockIsZt2({2}),
        "DT_one",StockIsDt2({2}),
        "ZT",StockIsZt({2}),
        "DT",StockIsDt({2}),
        "ever_ZT",StockIsCJZt({2}),
        "ever_DT",StockIsCJDt({2}),
        "Total_value",StockTotalValue3(),
        "Total_liq_value",StockMarketValue3(),
        "PE_TTM",StockPE3_V(0),
        "PB",StockPNA3_II(),
        "PS",StockPMI3_V(),
        "PC",StockPCF3_V(),
        "PTB",StockPTBR3_II(),
        "issue_date",StockGoMarketDate());
        """

    base_data_column = ["stock_code",
                        "stock_name",
                        "high",
                        "low",
                        "pre_close",
                        "close",
                        "open",
                        "pct_chg",
                        "turn",
                        "volume_ratio",
                        "log_return",
                        "is_down",
                        "is_up",
                        "is_equal",
                        "ZT_one",
                        "DT_one",
                        "ZT",
                        "DT",
                        "ever_ZT",
                        "ever_DT",
                        "Total_value",
                        "Total_liq_value",
                        "PE_TTM",
                        "PB",
                        "PS",
                        "PC",
                        "PTB",
                        "date",
                        "issue_date"]
    # wind_code, sec_name, implementation_d, name_before, name_after, reason, sec_type
    # ----------------start special treated stock------------------------
    createSQL_startST = 'create table if not exists startST( \
                            stock_code char(10) NOT NULL,\
                            stock_name char(10) NOT NULL,\
                            date date NOT NULL,\
                            name_before char(10) NOT NULL,\
                            name_after char(10) NOT NULL,\
                            reason varchar(60) NOT NULL,\
                            sec_type char(10) NOT NULL\
                            );'

    startST_column = ["stock_code",
                      "stock_name",
                      "date",
                      "name_before",
                      "name_after",
                      "reason",
                      "sec_type"]

    # wind_code, sec_name, implementation_d, name_before, name_after, sec_type
    # -----------------end special treated stock--------------------------
    createSQL_endST = 'create table if not exists endST(\
                            stock_code char(10) NOT NULL,\
                            stock_name char(10) NOT NULL,\
                            date date NOT NULL,\
                            name_before char(10) NOT NULL,\
                            name_after char(10) NOT NULL,\
                            sec_type char(10) NOT NULL\
                            );'

    endST_column = ["stock_code",
                    "stock_name",
                    "date",
                    "name_before",
                    "name_after",
                    "sec_type"]

    # ------------- trade_suspend tables -------------
    createSQL_trade_suspend = 'create table if not exists trade_suspend( \
                                date date NOT NULL,\
                                stock_code char(10) NOT NULL,\
                                stock_name char(10) NOT NULL,\
                                suspend_type varchar(20),\
                                suspend_reason varchar(60) NOT NULL,\
                                primary key(date, stock_code)\
                                );'

    trade_suspend_column = ["date",
                            "stock_code",
                            "stock_name",
                            "suspend_type",
                            "suspend_reason"]

    # ------------- trade resume tables -------------
    createSQL_trade_resume = 'create table if not exists trade_resume ( \
                                date date NOT NULL,\
                                stock_code char(10) NOT NULL,\
                                stock_name char(10) NOT NULL,\
                                primary key(date,stock_code)\
                                );'

    trade_resume_column = ["date",
                           "stock_code",
                           "stock_name"]

    start_end_dict = {"startST": startST_column,
                      "endST": endST_column,
                      "trade_suspend": trade_suspend_column,
                      "trade_resume": trade_resume_column}

    base_special_column = ["ZT_one",
                           "DT_one",
                           "ZT",
                           "DT",
                           "ever_ZT",
                           "ever_DT"]

    wind_fields = {"startST": "carryoutspecialtreatment",
                   "endST": "cancelspecialtreatment",
                   "suspend": "tradesuspend",
                   "resume": "traderesume"}

    # ------------- create  financial tables-------------
    # @staticmethod

    profitability = """
        return 
        Query("","{0}",True,"",
        "stock_code",DefaultStockID(),
        "stock_name",CurrentStockName(),
        "净资产收益率",reportofall(9900100,{1}),
        "扣除非经常损益后的净资产收益率",reportofall(9900101,{1}),
        "销售净利率",reportofall(9900102,{1}),
        "销售毛利率",reportofall(9900103,{1}),
        "销售税金率",reportofall(9900104,{1}),
        "总资产净利率",reportofall(9900105,{1}),
        "主营业务利润率",reportofall(9900106,{1}),
        "营业利润率",reportofall(9900107,{1}),
        "净利润率",reportofall(9900108,{1}),
        "营业成本比例",reportofall(9900109,{1}),
        "营业费用比例",reportofall(9900110,{1}),
        "管理费用比例",reportofall(9900111,{1}),
        "财务费用比例",reportofall(9900112,{1}),
        "三项费用比例",reportofall(9900113,{1}),
        "成本费用利润率",reportofall(9900114,{1}),
        "股东权益收益率",reportofall(9900115,{1}),
        "总资产报酬率",reportofall(9900116,{1}),
        "三项费用合计",reportofall(9900117,{1}),
        "营业外收支净额",reportofall(9900118,{1}),
        "营业成本合计",reportofall(9900119,{1}),
        "资本报酬率",reportofall(9900120,{1}),
        "营运报酬率",reportofall(9900121,{1}),
        "销售毛利",reportofall(9900122,{1}));
        """

    profitability_column = ["stock_code",
                            "stock_name",
                            "净资产收益率",
                            "扣除非经常损益后的净资产收益率",
                            "销售净利率",
                            "销售毛利率",
                            "销售税金率",
                            "总资产净利率",
                            "主营业务利润率",
                            "营业利润率",
                            "净利润率",
                            "营业成本比例",
                            "营业费用比例",
                            "管理费用比例",
                            "财务费用比例",
                            "三项费用比例",
                            "成本费用利润率",
                            "股东权益收益率",
                            "总资产报酬率",
                            "三项费用合计",
                            "营业外收支净额",
                            "营业成本合计",
                            "资本报酬率",
                            "营运报酬率",
                            "销售毛利",
                            "report_period"]

    createSQL_profitability = get_sql_statement('profitability', profitability_column)

    solvency = """
        return 
        Query("","{0}",True,"",
        "stock_code",DefaultStockID(),
        "stock_name",CurrentStockName(),
        "流动比率",reportofall(9900200,{1}),
        "速动比率",reportofall(9900201,{1}),
        "超速动比率",reportofall(9900202,{1}),
        "资产负债率",reportofall(9900203,{1}),
        "利息保障倍数",reportofall(9900204,{1}),
        "长期债务与营运资金比率",reportofall(9900205,{1}),
        "预收账款与营业收入比",reportofall(9900206,{1}),
        "营运资金",reportofall(9900207,{1}),
        "资产负债率扣预收账款后",reportofall(9900208,{1}));
        """

    solvency_column = ["stock_code",
                       "stock_name",
                       "流动比率",
                       "速动比率",
                       "超速动比率",
                       "资产负债率",
                       "利息保障倍数",
                       "长期债务与营运资金比率",
                       "预收账款与营业收入比",
                       "营运资金",
                       "资产负债率扣预收账款后",
                       "report_period"]

    createSQL_solvency = get_sql_statement("solvency", solvency_column)

    capital_structure = """
        return 
        Query("","{0}",True,"",
        "stock_code",DefaultStockID(),
        "stock_name",CurrentStockName(),
        "产权比率",reportofall(9900300,{1}),
        "股东权益比率",reportofall(9900301,{1}),
        "股东权益与固定资产比率",reportofall(9900302,{1}),
        "固定资产与股东权益比率",reportofall(9900303,{1}),
        "长期负债比例",reportofall(9900304,{1}),
        "固定资产比例",reportofall(9900305,{1}),
        "流动负债比",reportofall(9900306,{1}),
        "流动负债率",reportofall(9900307,{1}),
        "流动资产比例",reportofall(9900308,{1}),
        "权益负债比率",reportofall(9900309,{1}),
        "现金比",reportofall(9900310,{1}),
        "有形净值债务率",reportofall(9900311,{1}),
        "权益乘数杜邦",reportofall(9900312,{1}));
        """

    capital_structure_column = ["stock_code",
                                "stock_name",
                                "产权比率",
                                "股东权益比率",
                                "股东权益与固定资产比率",
                                "固定资产与股东权益比率",
                                "长期负债比例",
                                "固定资产比例",
                                "流动负债比",
                                "流动负债率",
                                "流动资产比例",
                                "权益负债比率",
                                "现金比",
                                "有形净值债务率",
                                "权益乘数杜邦",
                                "report_period"]

    createSQL_capital_structure = get_sql_statement("capital_structure", capital_structure_column)

    operational_capability = """
        return 
        Query("","{0}",True,"",
        "stock_code",DefaultStockID(),
        "stock_name",CurrentStockName(),
        "存货周转率",reportofall(9900400,{1}),
        "存货周转天数",reportofall(9900401,{1}),
        "存货增长率",reportofall(9900402,{1}),
        "存货销售比",reportofall(9900403,{1}),
        "应收账款周转率",reportofall(9900404,{1}),
        "应收账款周转天数",reportofall(9900405,{1}),
        "应收账款增长率",reportofall(9900406,{1}),
        "营业周期",reportofall(9900407,{1}),
        "流动资产周转率",reportofall(9900408,{1}),
        "流动资产周转天数",reportofall(9900409,{1}),
        "流动资产增长率",reportofall(9900410,{1}),
        "长期投资增长率",reportofall(9900411,{1}),
        "固定资产周转率",reportofall(9900412,{1}),
        "固定资产周转天数",reportofall(9900413,{1}),
        "固定资产增长率",reportofall(9900414,{1}),
        "无形资产及其它资产增长率",reportofall(9900415,{1}),
        "总资产周转率",reportofall(9900416,{1}),
        "总资产周转天数",reportofall(9900417,{1}),
        "总资产增长率",reportofall(9900418,{1}),
        "流动负债增长率",reportofall(9900419,{1}),
        "长期负债增长率",reportofall(9900420,{1}),
        "股东权益周转率",reportofall(9900421,{1}),
        "股东权益周转天数",reportofall(9900422,{1}),
        "净资产增长率",reportofall(9900423,{1}),
        "负债与股东权益增长率",reportofall(9900424,{1}),
        "应付账款周转率",reportofall(9900425,{1}),
        "应付账款周转天数",reportofall(9900426,{1}),
        "应付账款增长率",reportofall(9900427,{1}),
        "总资产周转率杜邦",reportofall(9900428,{1}),
        "非流动资产增长率",reportofall(9900429,{1}),
        "平均应收账款占营业收入",reportofall(9900430,{1}),
        "平均存货占营业成本",reportofall(9900431,{1}));
        """

    operational_capability_column = ["stock_code",
                                     "stock_name",
                                     "存货周转率",
                                     "存货周转天数",
                                     "存货增长率",
                                     "存货销售比",
                                     "应收账款周转率",
                                     "应收账款周转天数",
                                     "应收账款增长率",
                                     "营业周期",
                                     "流动资产周转率",
                                     "流动资产周转天数",
                                     "流动资产增长率",
                                     "长期投资增长率",
                                     "固定资产周转率",
                                     "固定资产周转天数",
                                     "固定资产增长率",
                                     "无形资产及其它资产增长率",
                                     "总资产周转率",
                                     "总资产周转天数",
                                     "总资产增长率",
                                     "流动负债增长率",
                                     "长期负债增长率",
                                     "股东权益周转率",
                                     "股东权益周转天数",
                                     "净资产增长率",
                                     "负债与股东权益增长率",
                                     "应付账款周转率",
                                     "应付账款周转天数",
                                     "应付账款增长率",
                                     "总资产周转率杜邦",
                                     "非流动资产增长率",
                                     "平均应收账款占营业收入",
                                     "平均存货占营业成本",
                                     "report_period"]

    createSQL_operational_capability = get_sql_statement("operational_capability", operational_capability_column)

    growth_ability = """
        return 
        Query("","{0}",True,"",
        "stock_code",DefaultStockID(),
        "stock_name",CurrentStockName(),
        "营业收入增长率",reportofall(9900600,{1}),
        "主营利润增长率",reportofall(9900601,{1}),
        "营业利润增长率",reportofall(9900602,{1}),
        "利润总额增长率",reportofall(9900603,{1}),
        "净利润增长率",reportofall(9900604,{1}),
        "营业成本增长率",reportofall(9900605,{1}),
        "营业税金及附加增长率",reportofall(9900606,{1}),
        "其他利润增长率",reportofall(9900607,{1}),
        "营业费用增长率",reportofall(9900608,{1}),
        "管理费用增长率",reportofall(9900609,{1}),
        "财务费用增长率",reportofall(9900610,{1}),
        "三项费用增长率",reportofall(9900611,{1}),
        "投资收益增长率",reportofall(9900612,{1}),
        "补贴收入增长率",reportofall(9900613,{1}),
        "营业外收入增长率",reportofall(9900614,{1}),
        "营业外支出增长率",reportofall(9900615,{1}),
        "营业外收支净额增长率",reportofall(9900616,{1}),
        "所得税增长率",reportofall(9900617,{1}),
        "少数股东损益增长率",reportofall(9900618,{1}),
        "可供分配利润增长率",reportofall(9900619,{1}),
        "可供股东分配利润增长率",reportofall(9900620,{1}),
        "未分配利润增长率",reportofall(9900621,{1}));
        """

    growth_ability_column = ["stock_code",
                             "stock_name",
                             "营业收入增长率",
                             "主营利润增长率",
                             "营业利润增长率",
                             "利润总额增长率",
                             "净利润增长率",
                             "营业成本增长率",
                             "营业税金及附加增长率",
                             "其他利润增长率",
                             "营业费用增长率",
                             "管理费用增长率",
                             "财务费用增长率",
                             "三项费用增长率",
                             "投资收益增长率",
                             "补贴收入增长率",
                             "营业外收入增长率",
                             "营业外支出增长率",
                             "营业外收支净额增长率",
                             "所得税增长率",
                             "少数股东损益增长率",
                             "可供分配利润增长率",
                             "可供股东分配利润增长率",
                             "未分配利润增长率",
                             "report_period"]

    createSQL_growth_ability = get_sql_statement("growth_ability", growth_ability_column)

    cash_flow = """
        return 
        Query("","{0}",True,"",
        "stock_code",DefaultStockID(),
        "stock_name",CurrentStockName(),
        "销售现金比率",reportofall(9900700,{1}),
        "现金营业收入比率",reportofall(9900701,{1}),
        "现金净利润比率",reportofall(9900702,{1}),
        "现金总资产比率",reportofall(9900703,{1}),
        "现金流动负债比率",reportofall(9900704,{1}),
        "现金到期债务比率",reportofall(9900705,{1}),
        "现金总负债比率",reportofall(9900706,{1}),
        "现金股利保障倍数",reportofall(9900707,{1}),
        "债务保障率",reportofall(9900708,{1}),
        "销售商品及提供劳务收到的现金增长率",reportofall(9900709,{1}),
        "经营活动现金流量净额增长率",reportofall(9900710,{1}),
        "投资活动现金流量净额增长率",reportofall(9900711,{1}),
        "筹资活动现金流量净额增长率",reportofall(9900712,{1}),
        "现金及现金等价物的期末余额",reportofall(9900713,{1}),
        "现金流入合计",reportofall(9900714,{1}),
        "现金流出合计",reportofall(9900715,{1}));
        """

    cash_flow_column = ["stock_code",
                        "stock_name",
                        "销售现金比率",
                        "现金营业收入比率",
                        "现金净利润比率",
                        "现金总资产比率",
                        "现金流动负债比率",
                        "现金到期债务比率",
                        "现金总负债比率",
                        "现金股利保障倍数",
                        "债务保障率",
                        "销售商品及提供劳务收到的现金增长率",
                        "经营活动现金流量净额增长率",
                        "投资活动现金流量净额增长率",
                        "筹资活动现金流量净额增长率",
                        "现金及现金等价物的期末余额",
                        "现金流入合计",
                        "现金流出合计",
                        "report_period"]

    createSQL_cash_flow = get_sql_statement("cash_flow", cash_flow_column)

    report_issue = """
        return 
        Query("","{0}",True,"",
        "stock_code",DefaultStockID(),
        "stock_name",CurrentStockName(),
        "report_period",report(128001,{1}),
        "首次预约日期",report(128002,{1}),
        "实际披露日期",report(128006,{1}),
        "实际披露公布日",report(128011,{1}));
        """

    createSQL_report_issue = 'create table  if not exists report_issue( \
                                stock_code char(10) NOT NULL,\
                                stock_name char(10) NOT NULL,\
                                report_period date,\
                                首次预约日期 varchar(20),\
                                实际披露日期 varchar(20),\
                                实际披露公布日 varchar(20),\
                                primary key(stock_code, report_period)\
                                );'

    report_issue_column = ["stock_code",
                           "stock_name",
                           "report_period",
                           "首次预约日期",
                           "实际披露日期",
                           "实际披露公布日"]

    performance_forecast = """
        return 
        Query("","{0}",True,"",
        "stock_code",DefaultStockID(),
        "stock_name",CurrentStockName(),
        "report_period",report(40000,{1}),
        "issue_date",report(40001,{1}),
        "preview_type",report(40002,{1}),
        "preview_content",report(40003,{1}),
        "lower_bound",report(40005,{1}),
        "upper_bound",report(40006,{1}),
        "monetary_unit",report(40007,{1}),
        "比上年同期增长下限",report(40008,{1}),
        "比上年同期增长上限",report(40009,{1}),
        "数据来源",report(40011,{1}),
        "预警详情",report(40010,{1}));
        """

    createSQL_performance_forecast = 'create table if not exists performance_forecast(\
                                        stock_code char(10) NOT NULL,\
                                        stock_name char(10) NOT NULL,\
                                        report_period date, \
                                        issue_date date,\
                                        preview_type varchar(20),\
                                        preview_content text,\
                                        lower_bound float(18,4),\
                                        upper_bound float(18,4),\
                                        monetary_unit char(10),\
                                        比上年同期增长下限 float(18,4),\
                                        比上年同期增长上限 float(18,4),\
                                        数据来源 varchar(20),\
                                        预警详情 text,\
                                        primary key(stock_code,report_period)\
                                        );'

    performance_forecast_column = ["stock_code",
                                   "stock_name",
                                   "report_period",
                                   "issue_date",
                                   "preview_type",
                                   "preview_content",
                                   "lower_bound",
                                   "upper_bound",
                                   "monetary_unit",
                                   "比上年同期增长下限",
                                   "比上年同期增长上限",
                                   "数据来源",
                                   "预警详情"]

    performance_fast_report = """
        return 
        Query("","{0}",True,"",
        "stock_code",DefaultStockID(),
        "stock_name",CurrentStockName(),
        "report_period",report(41001,{1}),
        "issue_date",report(41002,{1}),
        "营业总收入",report(41003,{1}),
        "营业利润",report(41004,{1}),
        "利润总额",report(41005,{1}),
        "归属于母公司所有者净利润",report(41006,{1}),
        "基本每股收益",report(41007,{1}),
        "净资产收益率",report(41008,{1}),
        "资产总计",report(41009,{1}),
        "归属母公司股东权益合计",report(41010,{1}),
        "股本",report(41011,{1}),
        "每股净资产",report(41012,{1}));
        """

    createSQL_performance_fast_report = 'create table if not exists performance_fast_report(\
                                            stock_code char(10) NOT NULL,\
                                            stock_name char(10) NOT NULL,\
                                            report_period date,\
                                            issue_date date,\
                                            营业总收入 float(18,4),\
                                            营业利润 float(18,4),\
                                            利润总额 float(18,4),\
                                            归属于母公司所有者净利润 float(18,4),\
                                            基本每股收益 float(18,4),\
                                            净资产收益率 float(18,4),\
                                            资产总计 float(18,4),\
                                            归属母公司股东权益合计 float(18,4),\
                                            股本 float(18,4),\
                                            每股净资产 float(18,4), \
                                            primary key(stock_code, report_period)\
                                            );'

    performance_fast_report_column = ["stock_code",
                                      "stock_name",
                                      "report_period",
                                      "issue_date",
                                      "营业总收入",
                                      "营业利润",
                                      "利润总额",
                                      "归属于母公司所有者净利润",
                                      "基本每股收益",
                                      "净资产收益率",
                                      "资产总计",
                                      "归属母公司股东权益合计",
                                      "股本",
                                      "每股净资产"]

    financial_dict = {"profitability": profitability,
                      "solvency": solvency,
                      "capital_structure": capital_structure,
                      "operational_capability": operational_capability,
                      "growth_ability": growth_ability,
                      "cash_flow": cash_flow,
                      "report_issue": report_issue,
                      "performance_forecast": performance_forecast,
                      "performance_fast_report": performance_fast_report}

    financial_list = ["profitability",
                      "solvency",
                      "capital_structure",
                      "operational_capability",
                      "growth_ability",
                      "cash_flow",
                      "report_issue",
                      "performance_forecast",
                      "performance_fast_report"]

    financial_column_dict = {"profitability": profitability_column,
                             "solvency": solvency_column,
                             "capital_structure": capital_structure_column,
                             "operational_capability": operational_capability_column,
                             "growth_ability": growth_ability_column,
                             "cash_flow": cash_flow_column,
                             "report_issue": report_issue_column,
                             "performance_forecast": performance_forecast_column,
                             "performance_fast_report": performance_fast_report_column}

    createSQL_index_component = 'create table if not exists index_component(\
                                 weight float(18,4) NOT NULL,\
                                 stock_code char(10) NOT NULL,\
                                 date date NOT NULL,\
                                 stock_name char(10) NOT NULL,\
                                 weight_rank int(10) NOT NULL,\
                                 real_weight_date varchar(20) NOT NULL,\
                                 index_code char(10) NOT NULL,\
                                 index_name char(10) NOT NULL,\
                                 primary key(stock_code, date, index_code)\
                                 );'

    index_component_statement = """
        Ret:=GetBkWeightByDate('{0}', IntTodate({1}),t); 
        If Ret=true then 
             Return t 
        Else 
             Return '获取数据失败';
        """
    index_component_column = [['比例(%)',
                               '代码',
                               '截止日',
                               '名称',
                               '排名',
                               '指数成份日',
                               '指数代码',
                               '指数名称'],
                              ['weight',
                               'stock_code',
                               'date',
                               'stock_name',
                               'weight_rank',
                               'real_weight_date',
                               'index_code',
                               'index_name']]

    SW_industry_TSL_code_old = ['SW801010', 'SW801020', 'SW801030', 'SW801080',
                                'SW801110', 'SW801120', 'SW801130', 'SW801140',
                                'SW801150', 'SW801160', 'SW801170', 'SW801180',
                                'SW801200', 'SW801230', 'SW801050', 'SW801040',
                                'SW801210', 'SW801060', 'SW801070', 'SW801090',
                                'SW801190', 'SW801100']

    SW_industry_TSL_code_new = ['SW801200', 'SW801210', 'SW801230', 'SW801170',
                                'SW801160', 'SW801150', 'SW801140', 'SW801130',
                                'SW801120', 'SW801110', 'SW801080', 'SW801010',
                                'SW801020', 'SW801030', 'SW801040', 'SW801050',
                                'SW801180', 'SW801880', 'SW801790', 'SW801780',
                                'SW801770', 'SW801760', 'SW801750', 'SW801740',
                                'SW801730', 'SW801720', 'SW801710', 'SW801890']

    main_index_code = ['SH000300',
                       'SH000905',
                       'SH000016']


if __name__ == "__main__":
    print(get_sql_statement.__doc__)
    test = Admin.createSQL_cash_flow
    test1 = Admin.createSQL_growth_ability
    test2 = Admin.createSQL_profitability
    print('done')