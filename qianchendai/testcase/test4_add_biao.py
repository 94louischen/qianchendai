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
class TestAddBd(unittest.TestCase):
    excel = DoExcel(constant.excel_dir, 'add_biao')
    cases = excel.read_excel()

    @classmethod
    def setUpClass(cls):
        cls.resp = Request()
        cls.conf = DoConf(constant.globe_conf_dir)
        cls.con = DoMysql()

    @data(*cases)
    def test_add_bd(self, case):
        LogTools().info("当前执行的用例名称是:{}".format(case.title))
        case_data = context.param_replace(case.data)
        if case.check_sql:
            case_check_sql = context.param_replace(eval(case.check_sql)['sql1'])
            begin_count = self.con.read_fetchone(case_check_sql)['COUNT(*)']
            print(begin_count)
        url = 'http://' + self.conf.get_value('dev_info', 'domain_name') + self.conf.get_value('dev_info',
                                                                                               'path') + case.url
        res = self.resp.http_request(case.method, url, case_data, headers=case.headers)
        LogTools().info("响应信息是:{}".format(res.text))
        try:
            if res.json()['msg'] == '加标成功':
                new_count = self.con.read_fetchone(context.param_replace(eval(case.check_sql)['sql1']))['COUNT(*)']
                print(new_count)
                self.assertNotEqual(begin_count, new_count)
                #取借款用户所投标记录中的最大ID，并通过反射存在context类中，每投标成功一次覆盖context类中的load_id属性
                case_check_sql1 = context.param_replace(eval(case.check_sql)['sql2'])
                load_id_value = self.con.read_fetchone(case_check_sql1)['max(id)']
                setattr(context.Context, 'load_id', str(load_id_value))
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
