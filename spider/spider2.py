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
import gzip
import http.cookiejar
import re
import urllib.request


#保存成文件的函数
def saveMyFile(data):
    save_path='./data.txt'
    f_obj=open(save_path,'wb')
    f_obj.write(data)
    f_obj.close()
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

#如果没有 _xsrf, 我们或许有用户名和密码也无法登录知乎,这里是获取抓取到的数据里的XSRF值
def getXSRF(data):
    cer=re.compile(r'name=\"_xsrf\" value=\"(.*)\"', flags = 0)
    strlist=cer.findall(data)
    return strlist[0]

#第二种方法处理header好扩展， build_opener 这个方法, 用来自定义 opener, 这种方法的好处是可以方便的拓展功能,
'''
makeMyOpener 函数接收一个 head 参数, 这个参数是一个字典. 函数把字典转换成元组集合, 放进 opener. 这样我们建立的这个 opener 就有两大功能:
自动处理使用 opener 过程中遇到的 Cookies
自动在发出的 GET 或者 POST 请求中加上自定义的 Header
'''
def makeMyOpener(head):
    cook=http.cookiejar.CookieJar()#创建cookie对象
    pro=urllib.request.HTTPCookieProcessor(cook)
    opener=urllib.request.build_opener(pro)
    header=[]
    for key,value in head.items():
        elem=(key,value)
        header.append(elem)
        #print("header:",header)
    opener.addheaders=header
    return opener

#定义一个http头部
head = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}


url = 'http://www.zhihu.com/'
opener=makeMyOpener(head)
op=opener.open(url)
data=op.read()
data=my_Unzip(data)
_xsrf=getXSRF(data)
url+='login'
id='帐户'#可以通过抓包来分析一下
password='密码'
postDict={
    '_xsrf':_xsrf,
    'email':id,
    'password':password,
    'remeberme':'y'
    }
postDict={
    '_xsrf':_xsrf,
    'email':id,
    'password':password,
    'remeberme':'y'
    }
#把 字典 或者 元组集合 类型的数据转换成 & 连接的 str.
postdata=urllib.parse.urlencode(postDict).encode(encoding='utf_8', errors='ignore')
#print(postdata)#b'_xsrf=q123wrqwer&email=%E5%B8%90%E6%88%B7&password=%E5%AF%86%E7%A0%81&remeberme=y'
op=opener(url,postdata)
data=op.read()
data=my_Unzip(data)
saveMyFile(data)
print(data.decode())