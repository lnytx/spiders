# -*- coding=utf-8 -*-
'''
Created on 2017年4��11��

@author: ning.lin
'''
#抓取代理IP



from _collections import deque 
import random
import re
import string
import time
import urllib.request

from bs4 import BeautifulSoup
from django.contrib.sites import requests
import requests


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
#获取随机的header
header={"User-Agent":random.choice(user_agent_list)}
#定义一个函数，获取代理IP
def get_proxyIP():

    ip_list={}   #初始化列表用来存储获取到的IP
    url='http://haoip.cc/tiqu.htm'
    request=urllib.request.Request(url=url,headers=header)
    html=urllib.request.urlopen(request)
    data=html.read().decode('utf-8')
    soup=BeautifulSoup(data,'html.parser')
    iplistn=soup.findAll('div',class_='col-xs-12')
    for i in iplistn:
        ip=i.text.strip().strip()
        ip_list=ip.split()
        #print("ip_list",type(ip_list),ip_list)
    #获取随机的一个代理IP
    
    ip="".join(random.choice(ip_list)).strip()   #随机取IP并去除空格
    #print("获得的代理ip及端口",ip)
    #这是代理IP
    proxy={"http":ip}   #构造一个代理
    print("proxy",proxy)
    return proxy
#response=requests.get(url,headers=header,proxies=proxy,timeout=timeout)  #使用代理来获取response
#proxy_handler = urllib.request.ProxyHandler({'http': proxy_dict})  
#使用代理访问
def get_soup(url):
    proxy=get_proxyIP()
    #创建ProxyHandler
    proxy_handler = urllib.request.ProxyHandler(proxy)
    #创建Opener
    opener = urllib.request.build_opener(proxy_handler)
    #安装OPener
    urllib.request.install_opener(opener)  
    #添加User Angent
    req = urllib.request.Request(url=url, headers=header)
    #使用自己安装好的Opener
    respose=urllib.request.urlopen(req)
    html = respose.read().decode("utf-8")
    soup=BeautifulSoup(html,'html.parser')
    print(soup)
    local='D:\\tuba\\log.txt'
    with open(local,mode='r+', encoding='utf-8') as f:
        f.write(str(soup))
    return soup

#使用多线程访问
def max_therad(i):
    pass;

#异常时重试,状态不是200的URL重试多次
def url_retry(url,num_retries=3):  
    try:
        
        r = requests.get('http://www.itwhy.org')
        request = requests.get(url,timeout=60)  
        #raise_for_status(),如果不是200会抛出HTTPError错误  
        request.raise_for_status()  
        soup = get_soup(url)
    except request.HTTPError as e:
        soup=None
        write_err(e)
        with open('log.txt','a') as f:
            f.write()
        if num_retries>0:
            #如果不是200就重试，每次递减重试次数,使用函数获取soup数据
            return url_retry(url,num_retries-1)
    #如果url不存在会抛出ConnectionError错误，这个情况不做重试  
    except request.exceptions.ConnectionError as e:
        return  
    except request.exceptions.TimeOut:
        return
        
    return soup
#
def catchhref(url):
    queue = deque()
    visited = set()
    url = 'http://news.dbanotes.net'  # 入口页面, 可以换成别的
    queue.append(url)
    cnt = 0
    while queue:
        url = queue.popleft()  # 队首元素出队
        visited |= {url}  # 标记为已访问,放入队列中
        print('已经抓取: ' + str(cnt) + '   正在抓取 <---  ' + url)
        cnt += 1
        urlop = urllib.request.urlopen(url)
        if 'html' not in urlop.getheader('Content-Type'):
            continue
    # 避免程序异常中止, 用try..catch处理异常
        try:
            data = urlop.read().decode('utf-8')
        except:
            continue
      # 正则表达式提取页面中所有队列, 并判断是否已经访问过, 然后加入待爬队列
        linkre = re.compile('href=\"(.+?)\"')
        for x in linkre.findall(data):
            if 'http' in x and x not in visited:
                queue.append(x)
                print('加入队列 --->  ' + x)
            return queue
#写一些日志
def write_err(e):
    with open('log.txt','a') as f:
        logtime=time.strftime("%Y-%m-%d %H:%M:%S")
        print(logtime+'-----')
        f.write(str(logtime))
        f.write('\t')
        f.write(str(e))
        f.write('\n')
        