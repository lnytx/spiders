# -*- coding:utf-8 -*-
'''
Created on 2017��3��21��

@author: ning.lin
'''''

import os
import queue
import random
import urllib.request


qq = ''.join(str(random.choice(range(10))) for i in range(9) )
print(qq)

a=set('abcdefgadecgbcd')
print(a)
b=set('abchijk')
print(b)
print("a-b",a-b)#集合a中包含的元素（a独有的元素）
print("a|b",a|b)#集合a或b中包含的元素（合集）
print("a&b",a&b)#集合a和b中都包含的元素（交集）
print("a^b",a^b)#不同时包含于a和b的元素（交集取反）

url="http://www.csdn.net/"
a=urllib.request.urlopen(url)
#print("a.read()",a.read())

url='http://www.baidu.com/'
#处理header,不好扩展
req=urllib.request.Request(url,headers={
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    })
data=urllib.request.urlopen(req).read().decode('utf-8')
#print(data)

_xsrf='q123wrqwer'
url+='login'
id='帐户'#可以通过抓包来分析一下
password='密码'
postDict={
    '_xsrf':_xsrf,
    'email':id,
    'password':password,
    'remeberme':'y'
    }
#把 字典 或者 元组集合 类型的数据转换成 & 连接的 str.
postdata=urllib.parse.urlencode(postDict).encode(encoding='utf_8', errors='ignore')
#print(postdata)

#路径问题
dir=os.path.abspath('D:\Program Files\Python_Workspace\\test\爬虫图片')  
print("dir",dir)
work_path=os.path.join(dir,'tuba')
print("work_path",work_path)




