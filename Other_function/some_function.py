# -*- coding: utf-8 -*-
def format_date(x):
    try:
        return x.strftime('%Y%m%d')
    except TypeError:
        print('wrong input of {}'.format(x))


# 对pandas中dataframe的列按照指定顺序重新排列
def sort_df_columns(df, columns):
    import pandas as pd
    if not isinstance(df, pd.DataFrame):
        raise TypeError('df is a {0} not pd.DataFrame'.format(type(df)))
    elif not set(columns).issubset(set(list(df.columns))):
        raise ValueError('some column of columns not in df.columns')
    else:
        df_new = pd.DataFrame()
        for column in columns:
            df_new[column] = df[column]
    return df_new


def code_convert(code_list):
    """
    convert TSL stock code to wind stock code or reverse
    such as
    'SH000001' --> '000001.SH'
    or
    '000001.SH' --> 'SH000001'
    """
    def convert(code):
        if isinstance(code, str):
            if code[:2].isalpha():
                return code[2:] + '.' + code[:2]
            elif code[-2:].isalpha():
                return code[7:] + code[:6]
            else:
                raise ValueError("wrong input of %s" % code)
        else:
            raise TypeError('code input should be str not %s' % type(code))
    if isinstance(code_list, str):
        code_converted = convert(code_list)
        return code_converted
    elif isinstance(code_list, list):
        code_converted = list(map(convert, code_list))
        return code_converted
    else:
        raise TypeError('code_list input should be str or list not %s' % type(code_list))


if __name__ == '__main__':
    code_ = code_convert(['002466.SZ', '000001.SH'])
    print(code_)


