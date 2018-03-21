# -*- coding: utf-8 -*-
'''
Created on 2017��4��5��

@author: ning.lin

使用用户名与密码抓取http://www.zhihu.com/
需要xsrf值
压缩抓取后的数据
保存数据到本地
处理http头部信息

'''
from _collections import deque
import gzip
import http.cookiejar
import os
import re
import urllib.request


#定义一个http头部
head = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
#解压那些经过压缩后的页面
def my_Unzip(data):
#通过 opener.read() 读取回来的数据, 经过 ungzip 自动处理后, 再来一遍 decode() 就可以得到解码后的 str 了
    try:
        print("正在解压")
        data=gzip.decompress()
        print("解压完成")
    except:
        print("未经过压缩的数据")
    return data

#第二种方法处理header好扩展， build_opener 这个方法, 用来自定义 opener, 这种方法的好处是可以方便的拓展功能,
'''
makeMyOpener 函数接收一个 head 参数, 这个参数是一个字典. 函数把字典转换成元组集合, 放进 opener. 这样我们建立的这个 opener 就有两大功能:
自动处理使用 opener 过程中遇到的 Cookies
自动在发出的 GET 或者 POST 请求中加上自定义的 Header
'''
head = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
# def makeMyOpener(head,url):
#     cook=http.cookiejar.CookieJar()#创建cookie对象
#     opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cook))
#     header=[]
#     for key,value in head.items():
#         elem=(key,value)
#         header.append(elem)
#         #print("header:",header)
#     opener.addheaders=header
#     data=opener.open('http://news.dbanotes.net/', timeout=1000)
#     html=data.read().decode()
#     return html


#获取html数据
def getHtml(url):
    page=urllib.request.urlopen(url)
    html = page.read().decode()
    return html

#获取图片，并保存到本地
#用于在获取的整个页面中筛选需要的图片连接
def getImg(html):
    #reg = r'src="(.+?\.jpg)" pic_ext'
    #reg = r'src="([.*\S]*\.jpg)" pic_ext="jpeg"'
    #reg = r'src="(.+?\.jpg)" pic_ext'
    reg = r'img class="portrait " src="(.+?\.jpg)"'
    imgre=re.compile(reg)
    imglist=re.findall(imgre, html)
    #保存图片路径
    local='D:\\tuba\\'
    x=0
    for imgurl in imglist:
        print("imgurl",imgurl)
        urllib.request.urlretrieve(imgurl,local+'%s.jpg'%x)
        x+=1

#定义一个方法，获取输入页面所有的href里的超超连接，针对http://tieba.baidu.com，其他的页面需要再处理正则表达式
def catchhref(url):
    queue=deque()
    visited=set()
    queue.append(url)
    cnt=0
    headers={ 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0' }
    url=queue.popleft()#队列首部元素出列，相当于是读取一个url
    visited |={url}#将访问过的url放入集合中
    cnt +=1
    print('已经抓取'+str(cnt)+'正在抓取<---'+url)
    print("当前抓取",url)
    request=urllib.request.Request(url=url,headers=headers)
    urllop=urllib.request.urlopen(request)
    data=urllop.read().decode('utf-8',errors='ignore')
    linkre=re.compile('href="/p/\d+"')#通过找这些超链接去查看所有的链接页面
    print("linkre",linkre)
    for x in linkre.findall(data):
        lnk='http://tieba.baidu.com'+x[6:len(x)-1]+'/'
        queue.append(lnk)
    return queue

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

#利用队列与集合，不爬重复的url
def unique(queue):#queue里面全是队列
    visited=set()#定义一个集合
    for i in range(len(queue)):
        print(i,"这是queue中的url",queue[i])
        
    
    
url='http://tieba.baidu.com/p/1569069059/'
catchhref(url)
#print("getHtml",getHtml(url))
#imgurl https:https://tieba.baidu.com/p/5065760668
#getImg(getHtml(url))
print("queue",catchhref(url))
print("done")

