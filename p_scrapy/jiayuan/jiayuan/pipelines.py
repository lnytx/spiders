# -*- coding: utf-8 -*-
import json

import pymysql
import os
import re

import redis  
import requests
from scrapy import log
import scrapy.log


from jiayuan import settings
from settings import IMAGES_STORE
from scrapy  import  log
from jiayuan.items import JiayuanItem, PersonInfo, OtherItem


# from items import JiayuanItem,OtherItem
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
class JiayuanPipeline(object):
    def process_item(self, item, spider):
        return item



class Download_Imgs(object):
    def download_imgs(self,name_persionid,img_list):
        print("图片存放路径 ",IMAGES_STORE)
        imgPath=IMAGES_STORE  # 下载图片的保存路径
        img_dir = os.path.join(imgPath,self.parse_filename(name_persionid))
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        for i in range(len(img_list)):
            filename = os.path.join(img_dir,'_'+str(i)+'.jpg')
            try:
                with open(filename, 'wb') as handle:
                            response = requests.get(img_list[i], stream=True)
                            for block in response.iter_content(1024):
                                if not block:
                                    break
                                handle.write(block)
            except Exception as e:
                scrapy.log("图片保存失败 %s"%(img_list[i]), level=log.ERROR)
                
    def parse_filename(self,file_name):
        """
        :param path: 需要清洗的文件夹名字
        :return: 清洗掉Windows系统非法文件夹名字的字符串
        """
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_title = re.sub(rstr, "_", file_name)  # 替换为下划线
        return new_title
    def dict_parse_list(self,str1):
        #str1 = ['{"nick_name": "Katie", "heigth": "\\u5929\\u79e4\\u5ea7_165cm", "person_id": "4203064", "user_info": "36\\u5c81 \\u95f5\\u884c", "main_url": "http://www.jiayuan.com/4203064?fxly=pmtq-ss-211&pv.mark=s_p_c|4203064|0"}', '{"nick_name": "\\u7b80\\u8981", "heigth": "\\u72ee\\u5b50\\u5ea7_\\u6709\\u623f", "person_id": "24090595", "user_info": "44\\u5c81 \\u6df1\\u5733", "main_url": "http://www.jiayuan.com/24090595?fxly=pmtq-ss-211&pv.mark=s_p_c|24090595|0"}', '{"nick_name": "\\u8587\\u7433", "heigth": "\\u5927\\u4e13_\\u6709\\u623f", "person_id": "53732463", "user_info": "28\\u5c81 \\u6cb3\\u5317", "main_url": "http://www.jiayuan.com/53732463?fxly=pmtq-ss-211&pv.mark=s_p_c|53732463|0"}', '{"nick_name": "\\u6f2b\\u6b65\\u4e91\\u7aef", "heigth": "A\\u578b\\u8840_\\u6709\\u8f66", "person_id": "26926903", "user_info": "43\\u5c81 \\u897f\\u57ce", "main_url": "http://www.jiayuan.com/26926903?fxly=pmtq-ss-211&pv.mark=s_p_c|26926903|0"}', '{"nick_name": "love_wonderful", "heigth": "O\\u578b\\u8840_\\u672c\\u79d1", "person_id": "153498093", "user_info": "43\\u5c81 \\u9759\\u5b89", "main_url": "http://www.jiayuan.com/153498093?fxly=pmtq-ss-211&pv.mark=s_p_c|153498093|0"}', '{"nick_name": "crown", "heigth": "\\u6c49\\u65cf_\\u5c5e\\u9f99", "person_id": "43366684", "user_info": "30\\u5c81 \\u6df1\\u5733", "main_url": "http://www.jiayuan.com/43366684?fxly=pmtq-ss-211&pv.mark=s_p_c|43366684|0"}', '{"nick_name": "\\u9759", "heigth": "\\u6c34\\u74f6\\u5ea7_170cm", "person_id": "42257514", "user_info": "32\\u5c81 \\u9752\\u5c9b", "main_url": "http://www.jiayuan.com/42257514?fxly=pmtq-ss-211&pv.mark=s_p_c|42257514|0"}', '{"nick_name": "lanni-g", "heigth": "B\\u578b\\u8840_\\u672a\\u5a5a", "person_id": "2020988", "user_info": "35\\u5c81 \\u798f\\u5dde", "main_url": "http://www.jiayuan.com/2020988?fxly=pmtq-ss-211&pv.mark=s_p_c|2020988|0"}', '{"nick_name": "\\u837b\\u4e0a\\u5173\\u96ce", "heigth": "\\u5c5e\\u725b_\\u6709\\u623f", "person_id": "32041840", "user_info": "32\\u5c81 \\u6c99\\u576a\\u575d", "main_url": "http://www.jiayuan.com/32041840?fxly=pmtq-ss-211&pv.mark=s_p_c|32041840|0"}', '{"nick_name": "\\u67ad\\u67ad", "heigth": "\\u5c04\\u624b\\u5ea7_\\u6709\\u623f", "person_id": "29746383", "user_info": "36\\u5c81 \\u5317\\u789a", "main_url": "http://www.jiayuan.com/29746383?fxly=pmtq-ss-211&pv.mark=s_p_c|29746383|0"}', '{"nick_name": "\\u5723\\u84dd", "heigth": "O\\u578b\\u8840_\\u6c49\\u65cf", "person_id": "47139824", "user_info": "50\\u5c81 \\u666e\\u9640", "main_url": "http://www.jiayuan.com/47139824?fxly=pmtq-ss-211&pv.mark=s_p_c|47139824|0"}']
        '''
        将redis里的item(例如上面的str1)转换成可识别的dct
        '''
        print("str1",type(str1),len(str1))
        print("type",type(str1))
        result = []
        for i in range(len(str1)):
            print("i",i)
            result.append(json.loads(str1[i]))
        print("result",type(result),result)
        return result

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
                ret = self.cursor.fetchone()#获取第一行数据
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
    