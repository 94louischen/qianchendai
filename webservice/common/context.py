import re
import configparser
from common.ConfTools import DoConf
from common import constant
import datetime


class Context:
    Fverify_code = None


def param_replace(data):
    p = "#(.*?)#"

    while re.search(p, data):
        params = re.search(p, data)
        params1 = params.group(1)
        try:
            params2 = DoConf(constant.globe_conf_dir).get_value('data', params1)
        except configparser.NoOptionError as e:
            if hasattr(Context, params1):
                params2 = getattr(Context, params1)
            else:
                print("找不到相关值")
                raise e
        data = re.sub(p, params2, data, count=1)
    return data


# 如果验证码大于当前时间就减1天 (无数据库操作权限该方法调用不了)
def subtract_time(time):
    now_time = datetime.datetime.now()
    time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    if time > now_time:
        time = time - datetime.timedelta(days=1)
    return time


# 如果验证码小于当前时间就加2天 (无数据库操作权限该方法调用不了)
def add_time(time):
    now_time = datetime.datetime.now()
    time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    if time < now_time:
        time = time + datetime.timedelta(days=2)
    return time


if __name__ == '__main__':
    # test_data = "{'mobilephone': '#mobile#', 'pwd': '#pwd#'}"
    # result = param_replace(test_data)

    test_data = {"verify_code": "#Fverify_code#", "user_id": "louis", "channel_id": "1", "pwd": "123456",
                 "mobile": "#mobile#", "ip": "192.168.1.13"}
    print(test_data.items())
