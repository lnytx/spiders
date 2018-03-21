#-*-coding:utf-8-*-
'''
Created on 2017年4月11日

@author: admin
'''
import os
import random

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
proxy_ip=get_proxyIP()
print("proxy_ip",proxy_ip)

local="D:\\tuba\\"
url='http://pic1.sc.chinaz.com/Files/pic/face1/4649.jpg'
i=0
filename=os.path.join(local,str(i)+".jpg")
print("filename",filename)
def save_imgs(url,filename):
    img=url_open(url).content 
    with open(filename,'wb') as f:
        f.write(img)
def url_open(url):
    """
    爬取网页
    """
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    #req = requests.get(url=url,headers=headers,proxy_ip=get_proxyIP)
    req=requests.get(url,headers=header, timeout=10,proxies=proxy_ip)
    req.content
    req.encoding='utf8'
    r=req.text
    soup=BeautifulSoup(r,'html.parser')
    print(soup)
    return req
#save_imgs(url,filename)
url='http://tieba.baidu.com/f?kw=%E6%AC%A7%E7%BE%8E%E7%94%B5%E5%BD%B1&red_tag=v2981019520'
req=requests.get(url)
#r=req.text
print("cookies",req.cookies)
req.cookies
for i in req.cookies:
    print("name",i.name)
    print("value",i.value)
    
    
    
print({c.name:c.value for c in req.cookies})
print([c.value for c in req.cookies])


