import unittest
import random
from ddt import ddt, data
from common import context
from common import constant
from common.HttpRequest import Request
from common.ExcelTools import DoExcel
from common.ConfTools import DoConf
from common.LogTools import LogTools
from common.SqlTools import DoMysql

@ddt
class TestRegister(unittest.TestCase):
    excel = DoExcel(constant.excel_dir, 'register')
    cases = excel.read_excel()

    @classmethod
    def setUpClass(cls):
        cls.resp = Request()
        cls.con = DoMysql()
        cls.conf = DoConf(constant.globe_conf_dir)
        cls.log = LogTools(__name__)

    @data(*cases)
    def test_register(self, case):
        # self.log.info("当前执行的用例名称是:{}".format(case.title))
        self.log.mylog.info("当前执行的用例名称是:{}".format(case.title))
        case_data = eval(context.param_replace(case.data))

        if case.check_sql:
            case_check_sql = context.param_replace(case.check_sql)
            sql_result = self.con.read_fetchone(case_check_sql)
            mobile_param1 = int(sql_result['mobilephone']) + random.randint(1, 99)  # 原先的手机号加一个随机数
            case_data['mobilephone'] = str(mobile_param1)  # 替换字典中的key

        url = 'http://' + self.conf.get_value('dev_info', 'domain_name') + self.conf.get_value('dev_info',
                                                                                               'path') + case.url
        res = self.resp.http_request(case.method, url, case_data, headers=case.headers)
        # self.log.info("响应信息是:{}".format(res.text))
        self.log.mylog.info("响应信息是:{}".format(res.text))
        try:
            if res.json()['msg'] == '注册成功':
                sql = 'select MobilePhone from member where MobilePhone = ' + case_data['mobilephone']
                mobile_param2 = self.con.read_fetchone(sql)['MobilePhone']
                if mobile_param2 != self.conf.get_value('data', 'mobile'):  # 判断是否是原始登录手机号
                    sql = 'select MobilePhone from member where MobilePhone = ' + mobile_param2
                    query_mobile = self.con.read_fetchone(sql)
                    self.assertEqual(mobile_param2, query_mobile['MobilePhone'])  # 第二次注册判断
                    result = 'pass'
                else:
                    query_mobile = self.con.read_fetchone(sql)
                    self.assertEqual(case_data['mobilephone'], query_mobile['MobilePhone'])  # 第一次注册判断
                    result = 'pass'
                sql2 = 'select * from member where MobilePhone =' + case_data['mobilephone']
                member_id = str(self.con.read_fetchone(sql2)['id'])
                mobile_phone = str(self.con.read_fetchone(sql2)['mobilephone'])
                #把用户信息反射到context类，然后供后面的测试用例调用
                # mobile_pwd = str(self.con.read_fetchone(sql2)['pwd'])
                setattr(context.Context, 'member_id', member_id)
                setattr(context.Context, 'mobile_phone', mobile_phone)
                # setattr(context.Context, 'mobile_pwd', mobile_pwd)
            else:
                self.assertEqual(case.expected, res.text)
            result = 'pass'
        except AssertionError as e:
            result = 'fail'
            raise e
        finally:
            # self.log.info("响应结果是:{}".format(result))
            self.log.mylog.info("响应结果是:{}".format(result))
            self.excel.write_excel(case.case_id, res.text, result)

    @classmethod
    def tearDownClass(cls):
        cls.resp.close()
        cls.con.close()
