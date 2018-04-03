# -*- coding:utf-8 -*-
'''
Created on 2018年2月28日
@author: ning.lin
'''
'''
从redis读取数据
'''

import json
import os
import re
import urllib.parse

import redis  
import requests
from scrapy import log
import scrapy.log



pool=redis.ConnectionPool(host='127.0.0.1',port=6380,db=0,decode_responses=True)  #427条记录
r = redis.StrictRedis(connection_pool=pool)  
  
# keys = r.keys()  
# print (type(keys))
# print("keys",keys)
# 
# # # while True:
# # data = r.blpop(["jiayuan_main:items"])
# # # source = json.loads(data.decode("utf-8"))
# # print("data",type(data),data)
# 
# source = r.lrange('jiayuan_main:items',start=0,end=3)#11条数据
# print("source",type(source),len(source),source)
# print("转换",type(source[0]),source)
# data = json.loads(source)
# print("data",type(data),data)



def dict_parse_list(str1):
    #str1 = ['{"nick_name": "Katie", "heigth": "\\u5929\\u79e4\\u5ea7_165cm", "person_id": "4203064", "user_info": "36\\u5c81 \\u95f5\\u884c", "main_url": "http://www.jiayuan.com/4203064?fxly=pmtq-ss-211&pv.mark=s_p_c|4203064|0"}', '{"nick_name": "\\u7b80\\u8981", "heigth": "\\u72ee\\u5b50\\u5ea7_\\u6709\\u623f", "person_id": "24090595", "user_info": "44\\u5c81 \\u6df1\\u5733", "main_url": "http://www.jiayuan.com/24090595?fxly=pmtq-ss-211&pv.mark=s_p_c|24090595|0"}', '{"nick_name": "\\u8587\\u7433", "heigth": "\\u5927\\u4e13_\\u6709\\u623f", "person_id": "53732463", "user_info": "28\\u5c81 \\u6cb3\\u5317", "main_url": "http://www.jiayuan.com/53732463?fxly=pmtq-ss-211&pv.mark=s_p_c|53732463|0"}', '{"nick_name": "\\u6f2b\\u6b65\\u4e91\\u7aef", "heigth": "A\\u578b\\u8840_\\u6709\\u8f66", "person_id": "26926903", "user_info": "43\\u5c81 \\u897f\\u57ce", "main_url": "http://www.jiayuan.com/26926903?fxly=pmtq-ss-211&pv.mark=s_p_c|26926903|0"}', '{"nick_name": "love_wonderful", "heigth": "O\\u578b\\u8840_\\u672c\\u79d1", "person_id": "153498093", "user_info": "43\\u5c81 \\u9759\\u5b89", "main_url": "http://www.jiayuan.com/153498093?fxly=pmtq-ss-211&pv.mark=s_p_c|153498093|0"}', '{"nick_name": "crown", "heigth": "\\u6c49\\u65cf_\\u5c5e\\u9f99", "person_id": "43366684", "user_info": "30\\u5c81 \\u6df1\\u5733", "main_url": "http://www.jiayuan.com/43366684?fxly=pmtq-ss-211&pv.mark=s_p_c|43366684|0"}', '{"nick_name": "\\u9759", "heigth": "\\u6c34\\u74f6\\u5ea7_170cm", "person_id": "42257514", "user_info": "32\\u5c81 \\u9752\\u5c9b", "main_url": "http://www.jiayuan.com/42257514?fxly=pmtq-ss-211&pv.mark=s_p_c|42257514|0"}', '{"nick_name": "lanni-g", "heigth": "B\\u578b\\u8840_\\u672a\\u5a5a", "person_id": "2020988", "user_info": "35\\u5c81 \\u798f\\u5dde", "main_url": "http://www.jiayuan.com/2020988?fxly=pmtq-ss-211&pv.mark=s_p_c|2020988|0"}', '{"nick_name": "\\u837b\\u4e0a\\u5173\\u96ce", "heigth": "\\u5c5e\\u725b_\\u6709\\u623f", "person_id": "32041840", "user_info": "32\\u5c81 \\u6c99\\u576a\\u575d", "main_url": "http://www.jiayuan.com/32041840?fxly=pmtq-ss-211&pv.mark=s_p_c|32041840|0"}', '{"nick_name": "\\u67ad\\u67ad", "heigth": "\\u5c04\\u624b\\u5ea7_\\u6709\\u623f", "person_id": "29746383", "user_info": "36\\u5c81 \\u5317\\u789a", "main_url": "http://www.jiayuan.com/29746383?fxly=pmtq-ss-211&pv.mark=s_p_c|29746383|0"}', '{"nick_name": "\\u5723\\u84dd", "heigth": "O\\u578b\\u8840_\\u6c49\\u65cf", "person_id": "47139824", "user_info": "50\\u5c81 \\u666e\\u9640", "main_url": "http://www.jiayuan.com/47139824?fxly=pmtq-ss-211&pv.mark=s_p_c|47139824|0"}']
    '''
    将redis里的item(例如上面的str1)转换成可识别的dct
    '''
    print("str1",type(str1),len(str1))
    print("type",type(str1))
    result = []
    aaa = []
#     sss = json.loads(str1[0])
#     aaa = json.dumps(str1, ensure_ascii=False)    
#     print("aaa",type(aaa),aaa)
#     print("sssssss",type(sss),sss)
    for i in range(len(str1)):
        print("i",i)
        result.append(json.loads(str1[i]))
        for item in result:
            '''
            sql = 
            '''
            print("item",item)
#             aaa.append(item['nick_name'])
#             aaa.append(item['person_id'])
#             aaa.append(item['heigth'])
#             aaa.append(item['main_url'])
#             aaa.append(item['user_info'])
            
#         print("ss",type(json.loads(str1[i])),json.loads(str1[i]))
#         for k,v in json.loads(str1[i]).items():
#             aaa= tuple(result)
    #commit for结束后commit,否则速度很慢
    print("result",type(result),result)
    print("aaa",type(aaa),aaa)


def download_imgs(name_persionid,img_list):
    print("图片存放路径 ",IMAGES_STORE)
    imgPath=IMAGES_STORE  # 下载图片的保存路径
    img_dir = os.path.join(imgPath,parse_filename(name_persionid))
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

def parse_filename(file_name):
    """
    :param path: 需要清洗的文件夹名字
    :return: 清洗掉Windows系统非法文件夹名字的字符串
    """
    file_name = urllib.parse.unquote(file_name)#先将里面的16进制转换一下
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", file_name)  # 替换为下划线
    return new_title


# source = r.lrange('jiayuan_main:items',start=0,end=3)#11条数据
# print("source",type(source),len(source),source)
# print("转换",type(source[0]),source)
# data = json.loads(source)
# print("data",type(data),data)

if __name__=="__main__":
    str1 = '喂,要幸福\x0e_33岁_32595588'
    ss = parse_filename(str1)
    print("ss",ss)
#     dict_parse_list(source)
    #download_imgs('asf***',img_list)
# source = json.loads(data[1])
# print("单个字段",type(data[1]),data[1])
# print("source",type(source),source['person_id'])



