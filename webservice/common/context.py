import re
import configparser
from common.ConfTools import DoConf
from common import constant


class Context:
    member_id = None
    mobile_phone = None
    # mobile_pwd = None
    load_id = None


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


if __name__ == '__main__':
    test_data = "{'mobilephone': '#mobile#', 'pwd': '#pwd#'}"
    result = param_replace(test_data)
