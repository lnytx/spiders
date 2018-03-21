#-*- coding=utf-8 -*-
'''
Created on 2017��4��1��

@author: ning.lin
'''

import urllib.request

from bs4 import BeautifulSoup
import bs4
from django.http import response
from django.template.context_processors import request


url="http://www.csdn.net/"
a=urllib.request.urlopen(url)
#print("a.read()",a.read())
# print("type(a)",type(a))
# print("a.info",a.info)
# print("a.getcode",a.getcode)
values={'name':'voidking','language':'Python'}
#data是一个字典, 然后通过urllib.parse.urlencode()来将data转换为 ‘word=Jecvay+Notes’的字符串, 
#最后和url合并为full_url, 其余和上面那个最简单的例子相同. 
#data=urllib.parse.urlencode(values)#输出data <class 'str'> language=Python&name=voidking
data = urllib.parse.urlencode(values).encode(encoding='utf-8',errors='ignore')
#print("data",type(data),data)
headers={ 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0' }
request=urllib.request.Request(url=url, data=data,headers=headers,method='GET')#模拟通过浏览器访问，并添加http头部，防止被网站拒绝
respose=urllib.request.urlopen(request)
buffer=respose.read()
html=buffer.decode('utf-8')
print(html)
#full_url=url+url_values
#data=urllib.request.urlopen(url).read()
#data=data.decode('utf-8')
#print("data",data)

html_doc="""

"""
soup=BeautifulSoup(html_doc)
print(soup)