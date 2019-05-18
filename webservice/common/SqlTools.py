import pymysql
from common.ConfTools import DoConf
from common import constant
import datetime
from decimal import *


class DoMysql:

    def __init__(self, dbName):
        conf = DoConf(constant.globe_conf_dir)
        # 打开数据库连接
        self.db = pymysql.Connection(conf.get_value('dev_db', 'host'),
                                     conf.get_value('dev_db', 'username'),
                                     conf.get_value('dev_db', 'pwd'),
                                     conf.get_value('dev_db', dbName),
                                     cursorclass=pymysql.cursors.DictCursor)  # 将游标执行的结果以字典返回
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()

    # 把结果集的第一行以字典的形式返回
    def read_fetchone(self, sql):
        self.cursor.execute(sql)
        datas = self.cursor.fetchone()
        for key in datas:
            if isinstance(datas[key], datetime.date):
                datas[key] = datas[key].strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(datas[key], Decimal):
                datas[key] = str(datas[key])
        self.db.commit()
        return datas

    # 把多行结果以字典的形式返回一个大列表
    def read_fetchall(self, sql):
        self.cursor.execute(sql)
        datas = self.cursor.fetchall()
        self.db.commit()
        return datas

    # 修改数据库
    def update(self, sql):
        self.cursor.execute(sql)
        self.db.commit()

    def close(self):
        self.cursor.close()
        self.db.close()


if __name__ == '__main__':
    sql = "select * FROM t_mvcode_info_1 WHERE Fmobile_no = 18826587147"
    db = DoMysql()
    result = db.read_fetchone(sql)
    print(type(result['Fexpired_time']), result['Fexpired_time'])
