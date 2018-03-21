'''
Created on 2017年4月7日

@author: ning.lin
'''
# -*- coding: utf-8 -*-
'''
Created on 2017��4��5��

@author: ning.lin
'''
#定义一个方法来处理抓取动作，免得多个方法在同一个页面内不好处理

from _collections import deque
import http.cookiejar
import random
import re
import re
import time
import urllib.request

from django.contrib.sites import requests


def catchhref():
    url = 'http://tieba.baidu.com/p/1569069059/'
    h={'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0' }
    queue=deque()
    visited=set()
    queue.append(url)
    cnt=0
    url=queue.popleft()#队列首部元素出列，相当于是读取一个url
    visited |={url}#将访问过的url放入集合中
    cnt +=1
    print('已经抓取'+str(cnt)+'正在抓取<---'+url)
    print("当前抓取",url)
    request=urllib.request.Request(url=url,headers=h)
    urllop=urllib.request.urlopen(request)
    data=urllop.read().decode('utf-8',errors='ignore')
    linkre=re.compile('href="/p/\d+"')#通过找这些超链接去查看所有的链接页面
    print("linkre",linkre)
    for x in linkre.findall(data):
        print("x",x)
        lnk='http://tieba.baidu.com'+x[5:]+'/'
        print("link",lnk)
        queue.append(x)
        print("queue.len",len(queue))
        print("queue[0]",queue[0])
    return queue
# a=catchhref()
# print("a",len(a))
catchhref()

def proxy_ip():
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
    url='http://www.kuaidaili.com/proxylist/2/'
    reip=re.compile(r'data-title="IP">(.+?)<')
    ip_list=[]   #初始化列表用来存储获取到的IP
    hed=random.choice(user_agent_list)
    print("hed",hed)
    h={
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
    cook=http.cookiejar.CookieJar()
    opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cook))
    header=[]
    for key,value in h.items():
        elem=(key,value)
        header.append(elem)
        #print("header:",header)
    opener.addheaders=header
    data=opener.open(url)
    html=data.read()
    
#     request=urllib.request.Request(url=url,headers=h)
#     urllop=urllib.request.urlopen(request)
#     html=urllop.read().decode('utf-8',errors='ignore')
    
    
    
    print("html",html)
    reip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
    for ip in reip.findall(html):
        pass
    #print("html",html)
    iplistn=re.findall(r'r/>(.*?)<b',html,re.S)   #从html代码中获取所有/><b中的内容 re.S的意思是匹配包括所有换行符
    #print("iplistn",iplistn)
    for ip in iplistn:
        i=re.sub("\n","",ip)    #re.sub是re模块替换的方法，这表示将\n替换为空
        ip_list.append(i.strip())   #将IP添加到初始化列表中
        print("ip",ip)
    
proxy_ip()

    
