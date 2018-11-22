# -*- coding: utf-8 -*-

class DB_information:
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
                        "date"]

    base_special_column = ["ZT_one",
                           "DT_one",
                           "ZT",
                           "DT",
                           "ever_ZT",
                           "ever_DT"]

    trade_suspend_column = ["date",
                            "stock_code",
                            "stock_name",
                            "suspend_type",
                            "suspend_reason"]

    trade_resume_column = ["date",
                           "stock_code",
                           "stock_name"]
    startST_column = ["stock_code",
                      "stock_name",
                      "date",
                      "name_before",
                      "name_after",
                      "reason",
                      "sec_type"]
    endST_column = ["stock_code",
                    "stock_name",
                    "date",
                    "name_before",
                    "name_after",
                    "sec_type"]

