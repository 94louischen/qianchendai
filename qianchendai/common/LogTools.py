import logging
import os
from common import constant
from common.ConfTools import DoConf


class LogTools:

    def __init__(self, login_name):
        conf = DoConf(constant.globe_conf_dir)
        # 定义一个日志收集器
        self.mylog = logging.getLogger(login_name)
        # 设置收集级别
        self.mylog.setLevel(conf.get_value('log_level', 'info'))

        # 设置日志输出格式
        famatter = logging.Formatter(conf.get_value('log_format', 'format'))
        # 设置日志控制台输出
        hdr = logging.StreamHandler()
        hdr.setLevel(conf.get_value('log_level', 'info'))
        hdr.setFormatter(famatter)

        # 设置日志文件输出
        fdr = logging.FileHandler(os.path.join(constant.log_dir, 'log_info.log'), encoding='utf-8')
        fdr.setLevel(conf.get_value('log_level', 'info'))
        fdr.setFormatter(famatter)

        # 日志与收集器对接
        self.mylog.addHandler(hdr)
        self.mylog.addHandler(fdr)

if __name__ == '__main__':
    log = LogTools()
    log.info('测试数据123456')
    print("测试数据")
