'''
Created on 2017年5月26日

@author: ning.lin
'''
import gzip

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

header={
    'Connection':'Keep-Alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Host': 'www.egouexpress.com',
    'DNT': '1'
    }
id='lnytx'
password='ln123456'
postDict={
    'username':id,
    'password':password,
    'act':'act_login',
    'back_act':'http://www.egouexpress.com/index.php'
    }
url='http://www.egouexpress.com/user.php'
#get
def get_url():
    req=requests.get(url,params=postDict,headers=header)
    cookies = requests.utils.dict_from_cookiejar(req.cookies)
    print("url",req.url)
    print("cookies转成字典",cookies)
  ##可以通过保存文件的方式保存cookies
  #将字典转为CookieJar：
    cookies = requests.utils.cookiejar_from_dict(cookies, cookiejar=None, overwrite=True)
    print("字典转成CookieJar",cookies)
    #print("req.text",req.text)

#post
def post_url():
  req=requests.post(url,data=postDict,headers=header)
  #将CookieJar转为字典：
  cookies = requests.utils.dict_from_cookiejar(req.cookies)
  print("url",req.url)
  print("cookies转成字典",cookies)
  ##可以通过保存文件的方式保存cookies
  #将字典转为CookieJar：
  cookies = requests.utils.cookiejar_from_dict(cookies, cookiejar=None, overwrite=True)
  print("字典转成CookieJar",cookies)
  #print("req.text",req.text)
  
#url http://www.egouexpress.com/user.php?username=lnytx&password=ln123456&act=act_login&back_act=http%3A%2F%2Fwww.egouexpress.com%2Findex.php

if __name__=='__main__':
    post_url()

