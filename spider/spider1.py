# -*- coding: utf-8 -*-
'''
Created on 2017��4��5��

@author: ning.lin
'''
from _collections import deque
import http.cookiejar
import re
import urllib.request


url = 'http://news.dbanotes.net'
queue=deque()
visited=set()
queue.append(url)
cnt=0
headers={ 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0' }

#定义一个方法来处理抓取动作，免得多个方法在同一个页面内不好处理
def catch():
    while queue:
        url=queue.popleft()#队列首部元素出列，相当于是读取一个url
        visited |={url}#将访问过的url放入集合中
        cnt +=1
        print('已经抓取'+str(cnt)+'正在抓取<---'+url)
        print("当前抓取",url)
        request=urllib.request.Request(url=url,headers=headers)
        urllop=urllib.request.urlopen(request)
        if 'html' not in urllop.getheader('Content-Type'):#只抓取包含内容为html的页面
            continue
        #异常处理
        try:
            data=urllop.read().decode('utf-8',errors='ignore')
        except:
            url=queue.popleft()
        linkre=re.compile('href=\"(.+?)\"')#通过找这些超链接去查看所有的链接页面
        for x in linkre.findall(data):
            if 'http' in x and x not in visited:
                queue.append(x)
                print("加入队列--->",x)

#保存成文件的函数
def saveMyFile(data):
    save_path='./data.txt'
    f_obj=open(save_path,'wb')
    f_obj.write(data)
    f_obj.close()
#处理header,不好扩展
req=urllib.request.Request(url,headers={
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    })
oper1=urllib.request.urlopen(req)
data1=oper1.read()
#print(data.decode('utf-8'))
#第二种方法处理header好扩展， build_opener 这个方法, 用来自定义 opener, 这种方法的好处是可以方便的拓展功能,
def makeMyOpener(head = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}):
    cook=http.cookiejar.CookieJar()#创建cookie对象
    opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cook))
    header=[]
    for key,value in head.items():
        elem=(key,value)
        header.append(elem)
        #print("header:",header)
    opener.addheaders=header
    return opener
oper=makeMyOpener()
data=oper.open('http://news.dbanotes.net/', timeout=1000)
data=data.read()
print(data)
saveMyFile(data)



    