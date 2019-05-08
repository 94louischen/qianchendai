import unittest
from suds import WebFault
import warnings
from ddt import ddt, data
from common import context
from common import constant
from common.webservice import WebService
from common.ExcelTools import DoExcel
from common.ConfTools import DoConf
from common.LogTools import LogTools
from common.SqlTools import DoMysql


@ddt
class SendMCode(unittest.TestCase):
    excel = DoExcel(constant.excel_dir, 'SendMCode')
    cases = excel.read_excel()

    @classmethod
    def setUpClass(cls):
        cls.WS = WebService()
        cls.cf = DoConf(constant.globe_conf_dir)
        cls.log = LogTools(__name__)
        cls.log.mylog.info("开始测试")

    @data(*cases)
    def test_sendCode(self, case):
        self.log.mylog.info("当前执行的用例名称是:{}".format(case.title))
        url = "http://" + self.cf.get_value("dev_info", "domain_name") + ":" + self.cf.get_value("dev_info",
                                                                                                 "port") + case.url
        try:
            resp = self.WS.web_service(url, case.data)
        except WebFault as e:
            try:
                self.assertEqual(case.expected, e.fault.faultstring)
                resp = e.fault.faultstring
                warnings.simplefilter('ignore', ResourceWarning)
                result = "pass"
            except AssertionError as e:
                result = "fail"
                raise e
            finally:
                self.log.mylog.info("当前执行的用例执行是否通过:{}".format(result))
                self.excel.write_excel(case.case_id, str(resp), result)
        else:
            expected = eval(case.expected)
            try:
                self.assertEqual(expected["retCode"], resp.retCode)
                self.assertEqual(expected["retInfo"], resp.retInfo)
                result = "pass"
            except AssertionError as e:
                result = "fail"
                raise e
            finally:
                self.log.mylog.info("当前执行的用例执行是否通过:{}".format(result))
                self.excel.write_excel(case.case_id, str(resp), result)

    @classmethod
    def tearDownClass(cls):
        cls.log.mylog.info("结束测试")
