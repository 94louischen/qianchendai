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
class Investment(unittest.TestCase):
    excel = DoExcel(constant.excel_dir, 'Investment')
    cases = excel.read_excel()

    @classmethod
    def setUpClass(cls):
        cls.resp = Request()
        cls.conf = DoConf(constant.globe_conf_dir)
        cls.con = DoMysql()

    @data(*cases)
    def test_Investment(self, case):
        LogTools().info("当前用例标题是:{}".format(case.title))
        case_data = context.param_replace(case.data)
        if case.check_sql:
            case.check_sql = context.param_replace(case.check_sql)
            begin_LeaveAmount = self.con.read_fetchone(case.check_sql)['leaveamount']
            print("投资前的余额",begin_LeaveAmount)
        url = 'http://' + self.conf.get_value('dev_info', 'domain_name') + self.conf.get_value('dev_info',
                                                                                               'path') + case.url
        res = self.resp.http_request(case.method, url, case_data, headers=case.headers)
        LogTools().info("请求结果是:{}".format(res.text))
        try:
            if res.json()['msg'] == '竞标成功':
                new_LeaveAmount = self.con.read_fetchone(case.check_sql)['leaveamount']
                self.assertEqual(int(begin_LeaveAmount) - eval(case_data)['amount'], int(new_LeaveAmount))
            else:
                self.assertEqual(case.expected, res.text)
            result = 'pass'
        except AssertionError as e:
            result = 'fail'
            raise e
        finally:
            LogTools().info("响应结果是:{}".format(result))
            self.excel.write_excel(case.case_id, res.text, result)

    @classmethod
    def tearDownClass(cls):
        cls.resp.close()
