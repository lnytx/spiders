 
#-*-coding:utf-8-*- 
'''
Created on 2017年3朋16日

@author: ning.lin
'''
import mysql.connector
from mysql.connector import cursor
def connect():
    config={'host':'127.0.0.1',
                'user':'root',
                'password':'root',
                'port':3306,
                'database':'test',
                'charset':'utf8'
            }
    try:
        conn=mysql.connector.connect(**config)
        return conn
        print("conn is success!")
    except mysql.connector.Error as e:
        print("conn is fails{}".format(e))
    


# 创建表
def create_table():
    conn=connect()
    sql_create = "create table `python1`(`id` int(10),`name` varchar(20),`passwd` varchar(20))"
    sql2='drop table `python1`'
    cursor = conn.cursor()
    try:
        cursor.execute(sql2)
        cursor.execute(sql_create)
        print("create table success")
    except mysql.connector.Error as e:
        print("execute fails{}".format(e))
        
# 插入数据
def insert_table():
        try:
            conn=connect()
            cursor = conn.cursor()
            #直接字符串插入
            sql_insert1 = "insert into python1(id,name,passwd) values(1,'tom','strpass')"
            cursor.execute(sql_insert1)
            #元组连接插入方式
            sql_insert2 = "insert into python1(id,name,passwd) values(%s,%s,%s)"
            data = (2, 'jim', 'jimpasswd')
            cursor.execute(sql_insert2, data)
            #字典插入方式
            sql_insert3="insert into python1 (id,name,passwd) values(%(id)s,%(name)s,%(passwd)s)"
            data3={'id':6,'name':'jak','passwd':'passwdjsck'}
            cursor.execute(sql_insert3,data3)
            #MySQL Connector也支持多次插入
            sql_insert4 = "insert into python1(id,name,passwd) values(%s,%s,%s)"
            data4=[
                    (8,'jin','jin'),
                    (9,'yin','yinpass'),
                    (10,'hao','happass'),
                    (11,'中文','pass123')
                ]
            cursor.executemany(sql_insert4,data4)
            conn.commit()
        except mysql.connector.Error as e:
            print("execute fails{}".format(e))
        finally:
            cursor.close()
            conn.close()
            print("conn has chosed")

#查询语句
def select_table():
    sql_select='select id,name from python1 where id >%s'
    try:
        conn=connect()
        cursor=conn.cursor()
        cursor.execute(sql_select,(1,))
        for id,name in cursor:
            print("id is %s,name is %s" % (id,name))#ValueError: too many values to unpack (expected 2),因为前面查的是所有的字段
    except mysql.connector.Error as e:
        print("select cursor is faild".format(e))
#删除操作
def delete_table():
    sql_delete='delete from python1 where id=%(id)s and name=%(name)s'
    data={'id':2,'name':'jim'}
    try:
        conn=connect()
        cursor=conn.cursor()
        cursor.execute(sql_delete,data)
        conn.commit()
    except mysql.connector.Error as e:
        print("cursor is faild",e)
    finally:
        cursor.close()
        conn.close()
#create_table()
#insert_table()
#delete_table()
#select_table()

 
