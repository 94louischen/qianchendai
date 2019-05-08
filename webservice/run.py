# -*- coding:utf-8 -*-

import sys
import unittest
import HTMLTestRunnerNew
import os
from common import constant

sys.path.append('./')   #项目的根目录地址



class RunTestCase:

    def load_TestCase(self):
        case_dir = constant.case_dir
        discover = unittest.defaultTestLoader.discover(case_dir,pattern='test*.py')
        return discover

    def print_report(self,file):
        with open(file,'wb') as files:
            runner = HTMLTestRunnerNew.HTMLTestRunner(stream=files,title='测试报告',
                                                      description='前程贷的登录、注册、充值接口测试报告',tester='chenxuan')
            runner.run(self.load_TestCase())


if __name__ == '__main__':
    RunTestCase().print_report(os.path.join(constant.report_dir,'test_report.html'))




