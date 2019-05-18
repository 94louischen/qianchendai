import unittest
from ddt import ddt, data
from common import context
from common import constant
from common.webservice import WebService
from common.ExcelTools import DoExcel
from common.ConfTools import DoConf
from common.LogTools import LogTools
from common.SqlTools import DoMysql
from common.readom_card import IdNumber
import random


@ddt
class UserAuth(unittest.TestCase):
    excel = DoExcel(constant.excel_dir, 'userauth')
    cases = excel.read_excel()

    @classmethod
    def setUpClass(cls):
        cls.WS = WebService()
        cls.sql = DoMysql("dbName1")
        cls.cf = DoConf(constant.globe_conf_dir)
        cls.log = LogTools(__name__)
        cls.log.mylog.info("开始测试")
        setattr(context.Context, "cre_id", IdNumber.generate_id(random.randint(0, 1)))

    @data(*cases)
    def test_UserAuth(self, case):
        self.log.mylog.info("当前执行的用例名称是:{}".format(case.title))

        if case.check_sql:
            global count
            count = self.sql.read_fetchone(case.check_sql)["count(*)"]
        case_data = eval(context.param_replace(case.data))
        resp = self.WS.web_services(case.url, case_data, case.method)
        try:
            global result
            self.assertEqual(case.expected, resp)
            if resp == "ok":
                new_count = self.sql.read_fetchone(case.check_sql)["count(*)"]
                self.assertEqual(count, new_count - 1)
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
