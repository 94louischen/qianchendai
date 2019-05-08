import pymysql
from common.ConfTools import DoConf
from common import constant


class DoMysql:

    def __init__(self):
        conf = DoConf(constant.globe_conf_dir)
        # 打开数据库连接
        self.db = pymysql.Connection(conf.get_value('dev_db', 'host'),
                                     conf.get_value('dev_db', 'username'),
                                     conf.get_value('dev_db', 'pwd'),
                                     conf.get_value('dev_db', 'dbName'),
                                     cursorclass=pymysql.cursors.DictCursor)  #将游标执行的结果以字典返回
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()

    # 把结果集的第一行以字典的形式返回
    def read_fetchone(self, sql):
        self.cursor.execute(sql)
        datas = self.cursor.fetchone()
        self.db.commit()
        return datas

    # 把多行结果以字典的形式返回一个大列表
    def read_fetchall(self,sql):
        self.cursor.execute(sql)
        datas = self.cursor.fetchall()
        self.db.commit()
        return datas

    def close(self):
        self.cursor.close()
        self.db.close()


if __name__ == '__main__':
    sql = "SELECT * FROM member WHERE MobilePhone = 18826587140"
    db = DoMysql()
    result = db.read_fetchone(sql)
    print(type(result), result['leaveamount'])
    print(len(result))
