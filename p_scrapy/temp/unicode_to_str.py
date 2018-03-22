# -*- coding:utf-8 -*-
'''
Created on 2018年2月28日
@author: ning.lin
'''

import binascii
import datetime
from functools import partial
import json
import os

# i = 0
# f1 = '123.txt'
# f2='c.txt'
# # f = open('123.txt','r')
# #f2 = open('aaa.txt','w',encoding= 'utf8')
# 
# str1 = "\u771f\u771f"
# text = str1.encode('utf-8')
#   
# print ("码",text.decode('utf8')  )
#     
# ms = open(f1)  
# for line in ms.readlines():  
#     line = line.replace('##jiayser##','')
# #     line = line.encode('utf-8')
#     line = line.encode('utf-8').decode('unicode_escape')
#     print("line",line)
# #     s = json.JSONDecoder().decode(line)
# #     a =line.decode('utf8')
# #     print("aaa",type(a),a)
#     with open(f2,'w',encoding= 'utf8') as mon:  
#         mon.write(line)
if __name__=='__main__':
#     url = 'http://www.jiayuan.com/115187836?fxly=pmtq-ss-210&pv.mark=s_p_c|115187836|0'
#     aaa =   ['籍      贯：', '湖北十堰', '户      口：', '湖北十堰', '国      籍：', '中国大陆', '个性待征：', '有点内向', '幽  默 感：', '没有幽默感', '脾      气：', '偶尔会憋不住', '对待感情：', '一向认真对待感情', '是否要小孩：', '想要孩子', '何时结婚：', '顺其自然', '是否能接受异地恋：', '视情况而定', '理想婚姻：', '--愿与对方父母同住：', '不愿意', '家中排 行：', '老二', '父母情况：', '父母健在', '兄弟姐妹：', '1个哥哥', '父母经济情况：', '--', '父母医保情况：', '--', '父母 的工作：', '--']
#     print("url.rfind('/')",url.rfind('/'))
#     str1 = url[url.rfind('/')+1:url.index('?')]
#     print("ID",str1)
#     housework = []
#     pet = []
#     housework.append('家务未填写1')
#     housework.append('家务未填写2')
#     pet.append('未填写1')
#     pet.append ('未填写2')
#     print("housework",housework[0],housework[1])
#     print("pet",pet[0],pet[1])
    a = '五五_27_234325242'
    s = a[a.find('_')+1:a.rfind('_')]
    file = open("D:\\Program Files\\Python_Workspace\\spiders\\p_scrapy\\jiayuan\\jiayuan\\proxy_ip.txt_temp")
    print("s",s)
    while True:
        line = file.readline()
        print("line",line)
        if len(line)==0:break
#     a = {}
#     for i in range(len(aaa)):
#         if i%2==0:
#             a[aaa[i].replace(" ", "").replace("：", '')] = aaa[i+1]
#     print("a",type(a),a)