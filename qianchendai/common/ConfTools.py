# -*- coding:utf-8 -*-
from configparser import ConfigParser
from common import constant


class DoConf:

    def __init__(self, files):
        self.cf = ConfigParser()
        self.cf.read(files, encoding='utf-8')
        switch = self.cf.getboolean('switch', 'on')
        if switch:
            self.cf.read(constant.conf_test_dir, encoding='utf-8')
        else:
            self.cf.read(constant.conf_uat_dir, encoding='utf-8')

    def get_value(self, sections,options):
        value = self.cf.get(sections,options)
        return value


if __name__ == '__main__':
    dc = DoConf(constant.globe_conf_dir)
    print(dc.get_value('dev_db', 'host'))