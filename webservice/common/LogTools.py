import logging
import os
from common import constant
from common.ConfTools import DoConf


class LogTools:

    def __init__(self, log_name):
        conf = DoConf(constant.globe_conf_dir)
        # 定义一个日志收集器
        self.mylog = logging.getLogger(log_name)
        # 设置收集级别
        self.mylog.setLevel(conf.get_value('log_level', 'debug'))

        # 设置日志输出格式
        famatter = logging.Formatter(conf.get_value('log_format', 'format'))
        # 设置日志控制台输出
        hdr = logging.StreamHandler()
        hdr.setLevel(conf.get_value('log_level', 'debug'))
        hdr.setFormatter(famatter)

        # 设置日志文件输出
        fdr = logging.FileHandler(os.path.join(constant.log_dir, 'log_info.log'), encoding='utf-8')
        fdr.setLevel(conf.get_value('log_level', 'debug'))
        fdr.setFormatter(famatter)

        # 收集渠道与日志收集器
        self.mylog.addHandler(hdr)
        self.mylog.addHandler(fdr)


if __name__ == '__main__':
    log = LogTools(__name__)
    log.info('测试数据123456')
    print("测试数据")
