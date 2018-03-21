'''
Created on 2017年4月11日

@author: ning.lin
'''
import random
import time
import urllib.request

from bs4 import BeautifulSoup


list1=['a','b','c']
list2=['123456']
print(random.choice(list1))
print(random.choice(list2))

with open('log.txt','a') as f:
    for i in range(10):
        logtime=time.strftime("%Y-%m-%d %H:%M:%S")
        print(logtime+'-----')
        f.write(str(logtime))
        f.write('\t')
        f.write(str(i))
        f.write('\n')
        


#header={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3'}

h = [('Accept', 'image/png, image/svg+xml, image/jxr, image/*; q=0.8, */*; q=0.5'),
   ('Accept-Encoding', 'gzip, deflate'),
   ('Accept-Language', 'zh-CN'),
   ('Connection', 'Keep-Alive'),
   ('Host', 'ww1.sinaimg.cn'),
   ('If-Modified-Since', 'Mon, 08 Jul 2013 18:06:40 GMT'),
   ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko')]
print(type(h))
def get_soup(url):
    cnt=0
    headers={('Host', 'ww1.sinaimg.cn'),
             ('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'),
             ('If-Modified-Since', 'Mon, 08 Jul 2013 18:06:40 GMT') }
    h={'User_Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2723.3 Safari/537.36',
    'Host': 'ww1.sinaimg.cn',
    'Referer':'http://www.google.com'}
    request=urllib.request.Request(url=url,headers=h)
    req=urllib.request.urlopen(request)
    data=req.read().decode('utf-8',errors='ignore')
    soup=BeautifulSoup(data,'html.parser')
    return soup
    
    # headers={ 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0' }
# req=urllib.request.Request(url=url,headers=headers)
# html=urllib.request.urlopen(req)
# data=html.read()
    
    
def get_image(url,filename):
    """
     从单独的页面中提取出图片保存为filename
    """
    soup=get_soup(url)
#     image=[]
#     reg = r'img class="portrait " src="(.+?\.jpg)"'
#     imgre=re.compile(reg)
    #imglist=re.findall(imgre, html)
    a=soup.find_all('img',style="cursor:pointer;")#[0].find_all('img')[0]['src']
    for i in a:
        #获取页面里的图片的地址
        imgurl=i['src']
        print(imgurl)
        urllib.request.urlretrieve(imgurl,filename)
    print("done")
local='D:\\tuba\\aaa,jpg'
get_image('https://www.ff564.com/htm/pic7/109654.htm',local)