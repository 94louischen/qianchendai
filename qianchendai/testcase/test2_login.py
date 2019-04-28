import unittest
from ddt import ddt, data
from common import constant
from common.HttpRequest import Request
from common.ExcelTools import DoExcel
from common.ConfTools import DoConf
from common.LogTools import LogTools
from common import context


@ddt
class TestLogin(unittest.TestCase):
    excel = DoExcel(constant.excel_dir, 'login')
    cases = excel.read_excel()

    @classmethod
    def setUpClass(cls):
        cls.resp = Request()
        cls.conf = DoConf(constant.globe_conf_dir)

    @data(*cases)
    def test_login(self, case):
        LogTools().info("当前执行的用例名称是:{}".format(case.title))
        case_data = context.param_replace(case.data)
        url = 'http://' + self.conf.get_value('dev_info', 'domain_name') + self.conf.get_value('dev_info',
                                                                                               'path') + case.url
        res = self.resp.http_request(case.method, url, case_data, headers=case.headers)
        LogTools().info("响应信息是:{}".format(res.text))
        try:
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
