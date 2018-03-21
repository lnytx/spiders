'''
Created on 2017年5月26日

@author: ning.lin
'''

import gzip
from http import cookiejar
import http.cookiejar
from urllib import request
import urllib

import requests


#解压缩
def ungzip(data):
    try:        # 尝试解压
        print('正在解压.....')
        data = gzip.decompress(data)
        print('解压完毕!')
    except:
        print('未经压缩, 无需解压')
    return data
#处理头部信息
def getOpener(head):
    global cj
    # 初始化一个CookieJar来处理Cookie
    cj=http.cookiejar.CookieJar()
    #实例化一个全局opener
    handler=urllib.request.HTTPCookieProcessor(cj)
    opener=urllib.request.build_opener(handler)
    header=[]
    for key,value in head.items():
        elem=(key,value)
        header.append(elem)
    opener.addheaders=header
    return opener

header={
    'Connection':'Keep-Alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Host': 'www.egouexpress.com',
    'DNT': 1
    }
url='http://www.egouexpress.com/'
opener=getOpener(header)
op=opener.open(url)
data=op.read()
data=ungzip(data)
url +='user.php'

id='lnytx'
password='ln123456'
postDict={
    'username':id,
    'password':password,
    'act':'act_login',
    'back_act':'http://www.egouexpress.com/index.php'
    }
postData=urllib.parse.urlencode(postDict).encode()

print("postData",postData)

op=opener.open(url,postData)

#打印cookies
for item in cj:
    print("name=%s" % item.name)
    print("value=%s"% item.value)
#保存cookies
#设置保存cookie的文件，同级目录下的cookie.txt
filename = 'cookie.txt'
#声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
cookie = cookiejar.MozillaCookieJar(filename)
#利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
handler=request.HTTPCookieProcessor(cookie)
#通过CookieHandler创建opener
opener = request.build_opener(handler)
#此处的open方法打开网页
response = opener.open('http://www.egouexpress.com/index.php')
#保存cookie到文件
cookie.save(ignore_discard=True, ignore_expires=True)

data=op.read()
data=ungzip(data)
#print("data",data.decode())
