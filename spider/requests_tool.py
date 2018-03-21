'''
Created on 2017年4月11日

@author: admin
'''
from _collections import deque
import os
import random
import re
import socket
import time

from bs4 import BeautifulSoup
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
print("hdader",header)
#获取代理IP
def get_proxyIP():

    ip_list={}   #初始化列表用来存储获取到的IP
    url='http://haoip.cc/tiqu.htm'
    req=requests.get(url=url,headers=header)
    r=req.text
    soup=BeautifulSoup(r,'html.parser')
    iplistn=soup.findAll('div',class_='col-xs-12')
    for i in iplistn:
        ip=i.text.strip().strip()
        ip_list=ip.split()
        print("ip_list",type(ip_list),ip_list)
    #获取随机的一个代理IP
    ip="".join(random.choice(ip_list)).strip()   #随机取IP并去除空格
    #print("获得的代理ip及端口",ip)
    #这是代理IP
    proxy={"http":ip}   #构造一个代理
    print("proxy",proxy)
    return proxy
#使用代理IP访问url
def get_soup(url,retry=5):
    #根据上面的方法获取一个随机的代理IP
    proxy_ip=get_proxyIP()
    retry=10#设置重试次数
    timeout = 20    
    socket.setdefaulttimeout(timeout)#这里对整个socket层设置超时时间。后续文件中如果再使用到socket，不必再设置  
    sleep_download_time = 10  
    time.sleep(sleep_download_time) #这里时间自己设定  
    req=requests.get(url,headers=header, timeout=10,proxies=proxy_ip)
    try:
        r=req.text
        soup=BeautifulSoup(r,'html.parser')
        print(soup)
    except requests.HTTPError as e:
        soup=None
        write_err(e)
        print("retry",retry)
        #如果不是200就重试，每次递减重试次数,使用函数获取soup数据
            #如果url不存在会抛出ConnectionError错误，这个情况不做重试  
        return get_soup(url,retry-1)
       #如果url不存在会抛出ConnectionError错误，这个情况不做重试  
    except req.exceptions.ConnectionError as e:
        soup=None
        write_err(e)
        print("retry",retry)
        return get_soup(url,retry-1)  
    except req.exceptions.TimeOut:
        soup=None
        write_err(e)
        print("retry",retry)
        return get_soup(url,retry-1)
    finally:
        pass
        #req.close()
    return soup
    
#返回一个队列里面全是未爬取过的url
def catchhref(url,logfile):
    queue = deque()
    visited = set()
    #url = 'http://news.dbanotes.net'  # 入口页面, 可以换成别的
    queue.append(url)
    #将url写入文件中
    wqueue(url,logfile)
    cnt = 0
    while queue:
        url = queue.popleft()  # 队首元素出队
        visited |= {url}  # 标记为已访问
        #并将其写入set文件中
        wqueue(url,'D:\\tuba\\set.txt')
        print(u'已经抓取: ' + str(cnt) + u'   正在抓取 <---  ' + url)
        cnt += 1
        try:
            #调用上面的方法获取soup对象
            soup=get_soup(url)
        except:
            continue
        #正则表达式提取页面中所有队列, 并判断是否已经访问过, 然后加入待爬队列
            linkre = re.compile('href=\"(.+?)\"')
            for x in linkre.findall(soup):
                print(x)  
                if 'http' in x and x not in visited:
                    queue.append(x)
                    wqueue(url,logfile)
                    print(u'写入队列 --->  ' + x)
        return visited
#写一些日志
def write_err(e):
    with open('log.txt','a') as f:
        logtime=time.strftime("%Y-%m-%d %H:%M:%S")
        print(logtime+'-----')
        f.write(str(logtime))
        f.write('\t')
        f.write(str(e))
        f.write('\n')
        
#将url写入队列
def wqueue(url,filename):
    with open(filename,'a') as f:
        f.write(url)
        f.write('\n')
#从队列中读取url
def rqueue(filename):
    list1=[]
    with open(filename,'r') as f:
        for line in f.readlines():
            list1.append([line.strip('\n')])
        return list1

#保存图片
def save_imgs(url,filename):
    dir_name=os.path.join(filename)
    if not os.path.exists(dir_name):
            os.mkdir(dir_name)
    try:
        img=get_image_urls(url).content 
        with open(filename,'wb') as f:
            f.write(img)
    except IOError as e:
        write_err(str(e))
        save_imgs(url,filename)
    finally:
        pass
def url_retry(url,num_retries=3):  
    try:
        r = requests.get('http://www.itwhy.org')
        request = requests.get(url,timeout=60)  
        #raise_for_status(),如果不是200会抛出HTTPError错误  
        request.raise_for_status()  
        soup = get_soup(url)
    except requests.HTTPError as e:
        soup=None
        write_err(e)
        with open('log.txt','a') as f:
            f.write()
        if num_retries>0:
            #如果不是200就重试，每次递减重试次数,使用函数获取soup数据
            return url_retry(url,num_retries-1)
    #如果url不存在会抛出ConnectionError错误，这个情况不做重试  
    except requests.exceptions.ConnectionError as e:  
        return  
    return soup
def get_image_urls(baseurl):
        pass   
filename='D:\\tuba\\queue.txt'
#print(rqueue(filename))

print("itemaaa",rqueue(filename)[1])
