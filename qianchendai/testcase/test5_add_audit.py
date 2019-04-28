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
class TestAudit(unittest.TestCase):
    excel = DoExcel(constant.excel_dir, 'audit')
    cases = excel.read_excel()

    @classmethod
    def setUpClass(cls):
        cls.resp = Request()
        cls.conf = DoConf(constant.globe_conf_dir)
        cls.con = DoMysql()

    @data(*cases)
    def test_audit(self, case):
        LogTools().info("当前执行的用例名称是:{}".format(case.title))
        case_data = context.param_replace(case.data)
        if case.check_sql:
            case.check_sql = context.param_replace(case.check_sql)
            begin_status = self.con.read_fetchone(case.check_sql)['status']
            print(begin_status)
        url = 'http://' + self.conf.get_value('dev_info', 'domain_name') + self.conf.get_value('dev_info',
                                                                                               'path') + case.url
        res = self.resp.http_request(case.method, url, case_data, headers=case.headers)
        LogTools().info("响应信息是:{}".format(res.text))
        try:
            if res.json()['code'] == "10001" and res.json()['status'] == 1 and res.json()['msg'] != "登录成功":
                new_status = self.con.read_fetchone(case.check_sql)
                print(new_status)
                self.assertNotEqual(begin_status, new_status['status'])
                result = 'pass'
                setattr(context.Context, 'load_id', str(new_status['id']))
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
        cls.con.close()



