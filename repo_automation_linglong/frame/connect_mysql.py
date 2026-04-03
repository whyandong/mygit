# -*- coding: utf-8 -*-
"""
连接数据库
"""

# -*- coding:utf8 -*

import pymysql

class MySQLHandler(object):

    def __init__(self):
        """初始化方法中，连接到数据库"""
        # 建立连接
        self.con = pymysql.connect(host='mysql-master-test.sndu.cn',
                                   port=3307,user='update_platform',
                                   password='update_platform',database='update_platform',
                                   cursorclass=pymysql.cursors.DictCursor
                                   )
        # 创建一个游标对象
        self.cur = self.con.cursor()
    def find_all(self,sql):
        #提交事务
        self.con.commit()
        #运行SQL语句 查询sql语句返回的所有数据
        self.cur.execute(sql)
        #运行的sql语句保存下来 所有数据 是一个元祖
        return self.cur.fetchall()
    def find_one(self,sql):
        #查询sql语句返回第一条数据
        self.con.commit()
        self.cur.execute(sql)
        return self.cur.fetchone()
    def find_count(self,sql):
        #sql语句查询的数据条数
        self.con.commit()
        res=self.cur.execute(sql)
        return res
    def updata(self,sql):
        self.cur.execute(sql)
        self.con.commit()
        return self.cur.execute(sql)

    def delete(self,sql):
        self.cur.execute(sql)
        self.con.commit()
        return self.cur.execute(sql)
    def close(self):
        #断开连接
       self.cur.close()
       self.con.close()

if __name__=='__main__':
    db = MySQLHandler()
    #res=db.updata("UPDATE `user` SET NickNameModifyCount = 1 where PhoneNumber='15007141571'")
    #res1=db.find_one("SELECT NickNameModifyCount FROM `user` where PhoneNumber='15007141571'")
    res2=db.delete("DELETE FROM terminal where device_id='case9257525'")
    #res3=db.delete("DETELE FROM `user` where Email='13285899299@gmail.com'")

    
















