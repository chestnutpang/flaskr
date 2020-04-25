from datetime import datetime


# 时间字符串转换为 datetime 格式时间
def ltimesf_str_to_datetime(gmt_time_string, strftime_format='%Y/%m/%d %H:%M:%S'):
    return datetime.strptime(gmt_time_string, strftime_format)
