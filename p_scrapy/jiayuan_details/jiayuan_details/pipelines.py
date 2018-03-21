# -*- coding: utf-8 -*-
import json

import pymysql
from scrapy  import  log

from jiayuan_details import settings
from jiayuan_details.items import JiayuanItem,PersonInfo,OtherItem


# from items import JiayuanItem,OtherItem
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
class JiayuanPipeline(object):
    def process_item(self, item, spider):
        return item


class JiayuanMysql(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            port=settings.MYSQL_PORT,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()
        #with open('/path/to/file', 'w',encoding='utf-8') as self.file:
            
    def process_item(self,item,spider):
        print("执行process_itemprocess_item")
        if item.__class__ == JiayuanItem:
            print("执行主搜索页面的sql")
            try:
                self.cursor.execute("""select * from main_user_info where main_url = %s""", item["main_url"])
                ret = self.cursor.fetchone()
                if ret:
                    self.cursor.execute(
                        """update main_user_info set person_id=%s, user_info = %s,nick_name = %s,main_url = %s,
                            heigth = %s  where main_url = %s""",
                        (item['person_id'],
                         item['user_info'],
                         item['nick_name'],
                         item['main_url'],
                         item['heigth'],
                         item['main_url']))
                else:
                    self.cursor.execute(
                        """insert into main_user_info(person_id,user_info,nick_name,main_url,heigth)
                          value (%s,%s,%s,%s,%s)""",
                        (item['person_id'],
                         item['user_info'],
                         item['nick_name'],
                         item['main_url'],
                         item['heigth']))
                self.connect.commit()
            except Exception as error:
                log(error)
        #可以添加多个item处理
        elif item.__class__ == PersonInfo:
            print("详情页面的sql")
            try:
                self.cursor.execute("""select * from person_info where person_id = %s""", item["person_id"])
                ret = self.cursor.fetchone()
                if ret:
                    self.cursor.execute(
                        """update person_info set person_id=%s, buy_car = %s,address = %s where person_id = %s""",
                        (item['person_id'],
                         item['buy_car'],
                         item['address'],
                         item['person_id']))
                else:
                    self.cursor.execute(
                        """insert into person_info(person_id,buy_car,address)
                          value (%s,%s,%s)""",
                        (item['person_id'],
                         item['buy_car'],
                         item['address']))
                self.connect.commit()
            except Exception as error:
                log(error)
                
        elif item.__class__ == OtherItem:
            pass
        else:
            pass
        return item
    #该方法在spider被开启时被调用。
    def open_spider(self, spider):
        pass
    #该方法在spider被关闭时被调用。
    def close_spider(self, spider):
        print("关闭")
    