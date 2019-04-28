import unittest
from ddt import ddt, data
from common import constant
from common.HttpRequest import Request
from common.ExcelTools import DoExcel
from common.ConfTools import DoConf
from common.LogTools import LogTools
from common.SqlTools import DoMysql
from common import context


@ddt
class TestRecharge(unittest.TestCase):
    excel = DoExcel(constant.excel_dir, 'recharge')
    cases = excel.read_excel()

    @classmethod
    def setUpClass(cls):
        cls.resp = Request()
        cls.conf = DoConf(constant.globe_conf_dir)
        cls.con = DoMysql()

    @data(*cases)
    def test_recharge(self, case):
        LogTools().info("当前执行的用例名称是:{}".format(case.title))
        case_data = context.param_replace(case.data)
        if case.check_sql:
            case.check_sql = context.param_replace(case.check_sql)
            begin_balance = self.con.read_fetchone(case.check_sql)['leaveamount']
            print(begin_balance)
        url = 'http://' + self.conf.get_value('dev_info', 'domain_name') + self.conf.get_value('dev_info',
                                                                                               'path') + case.url
        res = self.resp.http_request(case.method, url, case_data, headers=case.headers)
        LogTools().info("响应信息是:{}".format(res.text))
        try:
            if res.json()['msg'] == '充值成功':
                new_balance = self.con.read_fetchone(case.check_sql)['leaveamount']
                print(new_balance)
                self.assertEqual(int(begin_balance) + eval(case_data)['amount'], int(new_balance))
            else:
                self.assertEqual(case.expected, res.text)
            result = 'pass'
        except Exception as e:
            result = 'fail'
            raise e
        finally:
            LogTools().info("响应结果是:{}".format(result))
            self.excel.write_excel(case.case_id, res.text, result)

    @classmethod
    def tearDownClass(cls):
        cls.resp.close()
        cls.con.close()
