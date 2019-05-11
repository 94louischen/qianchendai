import os

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(root_dir)

conf_test_dir = os.path.join(root_dir, 'config', 'conf_test.cfg')

conf_uat_dir = os.path.join(root_dir, 'config', 'conf_uat.cfg')

globe_conf_dir = os.path.join(root_dir, 'config', 'globe_conf.cfg')

excel_dir = os.path.join(root_dir, 'data', 'cases.xlsx')

case_dir = os.path.join(root_dir, 'testcase')
print(case_dir)

report_dir = os.path.join(root_dir, 'report')

data_dir = os.path.join(root_dir, 'data')

log_dir = os.path.join(root_dir, 'log')
