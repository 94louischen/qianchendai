import unittest
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
    excel = DoExcel(constant.excel_dir, 'sendmcode')
    cases = excel.read_excel()

    @classmethod
    def setUpClass(cls):
        cls.WS = WebService()
        cls.sql = DoMysql("dbName")
        cls.cf = DoConf(constant.globe_conf_dir)
        cls.log = LogTools(__name__)
        cls.log.mylog.info("开始测试")
        setattr(context.Context, "mobile", context.create_phone())

    @data(*cases)
    def test_sendCode(self, case):
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
        else:
            if case.check_sql:
                sql_result = self.sql.read_fetchone(context.param_replace(case.check_sql))
                Fverify_code = sql_result["Fverify_code"]
                # 把验证码反射到context中的Context类
                setattr(context.Context, "Fverify_code", Fverify_code)
        finally:
            self.log.mylog.info("当前执行的用例执情况:{}".format(result))
            self.excel.write_excel(case.case_id, str(resp), result)

    @classmethod
    def tearDownClass(cls):
        cls.log.mylog.info("结束测试")
