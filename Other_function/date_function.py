# -*- coding: utf-8 -*-
# @Author  : chenyihui
# @Email   : chenyihui10@126.com
# @Time    :2018-6-25 14:36

from datetime import datetime, timedelta
# convert date to number and convert number to date


def date_to_num(date):
    date0 = datetime(2018, 6, 20)
    num0 = 43271
    if isinstance(date, datetime):
        day_diff = (date - date0).days
        result = num0 + day_diff
        return result
    elif isinstance(date, str):
        try:
            date = datetime.strptime(date, '%Y%m%d')
            day_diff = (date - date0).days
            result = num0 + day_diff
            return result
        except:
            print("%s input not a date" % date)
    elif isinstance(date, int):
        num_diff = date - num0
        result = (date0 + timedelta(num_diff)).strftime('%Y%m%d')
        return result
    else:
        print("wrong type of %s input" % date)


def get_index_update_date(year=None, update_type=None):
    """
    :param year:
    :param update_type
    :return:update_date
    每年的6月和12月的第二个星期五对300、500、50进行成分股调整
    获取 更新成分股的时间
    需要注意的是，wind中指数成分股更新是在下周一
    """

    def get_second_friday(month_start_day):
        week_day = month_start_day.weekday()
        if week_day < 4:
            second_friday = month_start_day + timedelta(week_day + 7)
        elif week_day == 4:
            second_friday = month_start_day + timedelta(7)
        else:
            second_friday = month_start_day + timedelta(6 - week_day + 14)
        return second_friday

    if year is None:
        year = datetime.today().year
    if update_type is None:
        mid = datetime(year, 6, 1)
        final = datetime(year, 12, 1)
        mid_update = get_second_friday(mid)
        final_update = get_second_friday(final)
        return [mid_update, final_update]
    elif update_type == 'half':
        mid = datetime(year, 6, 1)
        mid_update = get_second_friday(mid)
        return mid_update
    elif update_type == 'final':
        final = datetime(year, 6, 1)
        final_update = get_second_friday(final)
        return final_update


if __name__ == '__main__':
    print(get_index_update_date(year=2017))
    print(date_to_num('20180621'))
    print(date_to_num(datetime(2018, 6, 30)))
    print(date_to_num(43270))
    print(date_to_num('aa'))
    print(date_to_num(20.1))
