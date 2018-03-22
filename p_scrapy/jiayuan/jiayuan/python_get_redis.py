# -*- coding:utf-8 -*-
'''
Created on 2018年2月28日
@author: ning.lin
'''
'''
从redis读取数据写入mysql，并且根据item中的image的地址下载图片
'''

import json
import os
import random
import re

import pymysql
import redis  
import requests
from scrapy import log
import scrapy.log

from settings import IMAGES_STORE


pool=redis.ConnectionPool(host='127.0.0.1',port=6380,db=0,decode_responses=True)  #427条记录
r = redis.StrictRedis(connection_pool=pool)  
  




def connect():
    config={'host':'127.0.0.1',
                'user':'root',
                'password':'root',
                'port':3306,
                'database':'jiayuan',
                'charset':'utf8',
                #要加上下面一行返回的是list，否则默认返回的是tuple
                'cursorclass':pymysql.cursors.DictCursor,
            }
    try:
        conn=pymysql.connect(**config)
        print("conn is success!")
        return conn
    except Exception as e:
        print("conn is fails{}".format(e))


def dict_parse_list(str1):
    #str1 = ['{"nick_name": "Katie", "heigth": "\\u5929\\u79e4\\u5ea7_165cm", "person_id": "4203064", "user_info": "36\\u5c81 \\u95f5\\u884c", "main_url": "http://www.jiayuan.com/4203064?fxly=pmtq-ss-211&pv.mark=s_p_c|4203064|0"}', '{"nick_name": "\\u7b80\\u8981", "heigth": "\\u72ee\\u5b50\\u5ea7_\\u6709\\u623f", "person_id": "24090595", "user_info": "44\\u5c81 \\u6df1\\u5733", "main_url": "http://www.jiayuan.com/24090595?fxly=pmtq-ss-211&pv.mark=s_p_c|24090595|0"}', '{"nick_name": "\\u8587\\u7433", "heigth": "\\u5927\\u4e13_\\u6709\\u623f", "person_id": "53732463", "user_info": "28\\u5c81 \\u6cb3\\u5317", "main_url": "http://www.jiayuan.com/53732463?fxly=pmtq-ss-211&pv.mark=s_p_c|53732463|0"}', '{"nick_name": "\\u6f2b\\u6b65\\u4e91\\u7aef", "heigth": "A\\u578b\\u8840_\\u6709\\u8f66", "person_id": "26926903", "user_info": "43\\u5c81 \\u897f\\u57ce", "main_url": "http://www.jiayuan.com/26926903?fxly=pmtq-ss-211&pv.mark=s_p_c|26926903|0"}', '{"nick_name": "love_wonderful", "heigth": "O\\u578b\\u8840_\\u672c\\u79d1", "person_id": "153498093", "user_info": "43\\u5c81 \\u9759\\u5b89", "main_url": "http://www.jiayuan.com/153498093?fxly=pmtq-ss-211&pv.mark=s_p_c|153498093|0"}', '{"nick_name": "crown", "heigth": "\\u6c49\\u65cf_\\u5c5e\\u9f99", "person_id": "43366684", "user_info": "30\\u5c81 \\u6df1\\u5733", "main_url": "http://www.jiayuan.com/43366684?fxly=pmtq-ss-211&pv.mark=s_p_c|43366684|0"}', '{"nick_name": "\\u9759", "heigth": "\\u6c34\\u74f6\\u5ea7_170cm", "person_id": "42257514", "user_info": "32\\u5c81 \\u9752\\u5c9b", "main_url": "http://www.jiayuan.com/42257514?fxly=pmtq-ss-211&pv.mark=s_p_c|42257514|0"}', '{"nick_name": "lanni-g", "heigth": "B\\u578b\\u8840_\\u672a\\u5a5a", "person_id": "2020988", "user_info": "35\\u5c81 \\u798f\\u5dde", "main_url": "http://www.jiayuan.com/2020988?fxly=pmtq-ss-211&pv.mark=s_p_c|2020988|0"}', '{"nick_name": "\\u837b\\u4e0a\\u5173\\u96ce", "heigth": "\\u5c5e\\u725b_\\u6709\\u623f", "person_id": "32041840", "user_info": "32\\u5c81 \\u6c99\\u576a\\u575d", "main_url": "http://www.jiayuan.com/32041840?fxly=pmtq-ss-211&pv.mark=s_p_c|32041840|0"}', '{"nick_name": "\\u67ad\\u67ad", "heigth": "\\u5c04\\u624b\\u5ea7_\\u6709\\u623f", "person_id": "29746383", "user_info": "36\\u5c81 \\u5317\\u789a", "main_url": "http://www.jiayuan.com/29746383?fxly=pmtq-ss-211&pv.mark=s_p_c|29746383|0"}', '{"nick_name": "\\u5723\\u84dd", "heigth": "O\\u578b\\u8840_\\u6c49\\u65cf", "person_id": "47139824", "user_info": "50\\u5c81 \\u666e\\u9640", "main_url": "http://www.jiayuan.com/47139824?fxly=pmtq-ss-211&pv.mark=s_p_c|47139824|0"}']
    '''
    将redis里的item(例如上面的str1)转换成可识别的dct
    '''
    print("str1",type(str1),len(str1))
    print("type",type(str1))
    result = []
    for i in range(len(str1)):
        result.append(json.loads(str1[i]))
#         for item in result:
#             '''
#             sql = 
#             '''
#             print("item",item)
    return result


def download_imgs(name_persionid,img_list):
    
    '''
    为了防止封IP，下载图片这里也使用代理IP
    '''
    user_agent_list=[
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    header={"User-Agent":random.choice(user_agent_list)}
    ip={}
    f_ip = "D:\\Program Files\\Python_Workspace\\spiders\\p_scrapy\\test_spiders\\test_spiders\\proxy_ip.txt"
    with open (f_ip,'r') as f:
        for line in f.readlines():
            print("line",line)
            ip['http']=line
    
    print("图片存放路径 ",IMAGES_STORE)
    imgPath=IMAGES_STORE  # 下载图片的保存路径在settin中设置
    img_dir = os.path.join(imgPath,parse_filename(name_persionid))
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    for i in range(len(img_list)):#name_persionid[name_persionid.find('_')+1:name_persionid.rfind('_')]是取年龄的
        filename = os.path.join(img_dir,name_persionid[name_persionid.find('_')+1:name_persionid.rfind('_')]+'_'+str(i)+'.jpg')
        try:
            with open(filename, 'wb') as handle:
                response = requests.get(img_list[i], proxies=ip, headers=header)       
#                 response = requests.get(img_list[i], stream=True)
                for block in response.iter_content(1024):
                    if not block:
                        break
                    handle.write(block)
        except Exception as e:
            print("图片保存失败 %s" ,str(e))
           # scrapy.log("图片保存失败 %s"%(str(e)), level=log.ERROR)

def parse_filename(file_name):
    """
    :param path: 需要清洗的文件夹名字
    :return: 清洗掉Windows系统非法文件夹名字的字符串
    """
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", file_name)  # 替换为下划线
    return new_title


def sql_excute(data):
    '''
    为了保证速度，全部使用insert方式，不考虑重复，因为在scrapy_redis中已去除了重复的url了，理论上
    是没有重复数据的
    '''
    conn=connect()
    cursor=conn.cursor()
    sql_insert_economic_strength = "insert into economic_strength (person_id,salary,buy_house,buy_car,economic_concept,investment_financing,foreign_debt) \
                    values(%s,%s,%s,%s,%s,%s,%s)"
    
    sql_insert_life_style = "insert into life_style(person_id,smoke,drink_wine,exercise_habits,eating_habits,shopping,religious_belief,time_table,circle_of_communication,maximum_consumption,housework,household_assignment,pet,about_pets) \
                             values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
     
    sql_insert_marriage_concep = "insert into marriage_concep(person_id,address,registered_residence,nationality,personality,humor,temper,feelings,want_child,when_mary,strange_love,ideal_marriage,live_parents,rankings_home,parents_situation,brothers,parents_economic,parents_medical,parents_working) \
                                    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                                     
    sql_insert_mate_selection = "insert into mate_selection(person_id,age,height,nation,education,image,marital_status,address,sincerity) \
                                    values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    sql_insert_person_info = "insert into person_info(nike_name,person_id,province,age,municipal,age_info,education,height,buy_car,address,salary,housing,constellation,nation,weight,zodiac,blood_type,introduce_oneself,personality_label,interest_label,img_urls,url,image_dir) \
                                    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    sql_insert_work_study = "insert into work_study(person_id,position,company,company_type,welfare,working,transfer_work,work_family,overseas_job,university,major,language) \
                                    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    for item in data:
        try:
            #经济实力表
            cursor.execute(sql_insert_economic_strength, (item['person_id_economic'],item['salary_economic'],item['buy_house_economic'],item['buy_car_economic'],\
                       item['economic_concept'],item['investment_financing'],item['foreign_debt']))
            #生活方式表
            cursor.execute(sql_insert_life_style,(item['person_id_life'],item['smoke'],item['drink_wine'],item['exercise_habits'],\
                       item['eating_habits'],item['shopping'],item['religious_belief'],item['time_table'],item['circle_of_communication'],item['maximum_consumption'],item['housework'],\
                       item['household_assignment'],item['pet'],item['about_pets']))
            #婚姻态度表
            cursor.execute(sql_insert_marriage_concep,(item['person_id_marriage'],item['address_marriage'],item['registered_residence'],item['nationality'],\
                       item['personality'],item['humor'],item['temper'],item['feelings'],item['want_child'],item['when_mary'],item['strange_love'],\
                       item['ideal_marriage'],item['live_parents'],item['rankings_home'],item['parents_situation'],item['brothers'],item['parents_economic'],item['parents_medical'],item['parents_working']))
            #择偶标准表
            cursor.execute(sql_insert_mate_selection,(item['person_id_mate'],item['age_mate'],item['height_mate'],item['nation_mate'],\
                       item['education_mate'],item['image_mate'],item['marital_status'],item['address_mate'],item['sincerity_mate']))
            #个人信息表
            cursor.execute(sql_insert_person_info,(item['nike_name'],item['person_id'],item['province'],item['age'],item['municipal'],item['age_info'],item['education'],item['height'],item['buy_car'] \
                                               ,item['address'],item['salary'],item['housing'],item['constellation'],item['nation'],item['weight'],item['zodiac'],item['blood_type'],item['introduce_oneself'] \
                                              ,item['personality_label'],item['interest_label']," ".join(item['img_urls']),item['url'],item['image_dir']))#img_urls是list需要转成str
            #工作学习表
            cursor.execute(sql_insert_work_study,(item['person_id_study'],item['position'],item['company'],item['company_type'],item['welfare'],item['working'],item['transfer_work'],item['work_family'] \
                                              ,item['overseas_job'],item['university'],item['major'],item['language']))
        except Exception as e:
            print("执行错误，开始回滚",str(e))
            conn.rollback()
        finally:
            conn.commit()
if __name__=="__main__":
    print("当前有多少数据", r.llen('jiayuan_main:items'))
#     dict_parse_list(source)
    #img_list = ['http://at3.jyimg.com/23/d8/a1ec966844b8b5ba10646c1e807e/a1ec96684_1_avatar_square_p.jpg', 'http://t3.jyimg.com/23/d8/a1ec966844b8b5ba10646c1e807e/148225908d.jpg']
    start=0
    end=300
    total_num = r.llen('jiayuan_main:items')#总的item数量
    while total_num>0:
        print("jiayuan_main:items当前数量",total_num)
        source = r.lrange('jiayuan_main:items',start,end)#每取4条执行一次
        for item in dict_parse_list(source):
            download_imgs(parse_filename(item['image_dir']),item['img_urls'])
    #从redis写入数据库
        sql_excute(dict_parse_list(source))
        total_num -=300
#         start +=50
#         end +=4
    
# source = json.loads(data[1])
# print("单个字段",type(data[1]),data[1])
# print("source",type(source),source['person_id'])



