import unittest
from ddt import ddt, data
from common import context
from common import constant
from common.webservice import WebService
from common.ExcelTools import DoExcel
from common.ConfTools import DoConf
from common.LogTools import LogTools


@ddt
class BindCard(unittest.TestCase):
    excel = DoExcel(constant.excel_dir, 'bindcard')
    cases = excel.read_excel()

    @classmethod
    def setUpClass(cls):
        cls.WS = WebService()
        cls.cf = DoConf(constant.globe_conf_dir)
        cls.log = LogTools(__name__)
        cls.log.mylog.info("开始测试")

    @data(*cases)
    def test_BindCard(self, case):
        self.log.mylog.info("当前执行的用例名称是:{}".format(case.title))
        case_data = eval(context.param_replace(case.data))
        resp = self.WS.web_services(case.url, case_data, case.method)
        try:
            global result
            self.assertEqual(case.expected, resp)
            result = "pass"
        except AssertionError as e:
            result = "fail"
            raise e
        finally:
            self.log.mylog.info("当前执行的用例执情况:{}".format(result))
            self.excel.write_excel(case.case_id, str(resp), result)

    @classmethod
    def tearDownClass(cls):
        cls.log.mylog.info("结束测试")
