from _collections import deque
import re
import urllib.request


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
        #print("x",x,x[6:len(x)-1],len(x))
        lnk='http://tieba.baidu.com'+x[6:len(x)-1]+'/'
        #print("link",lnk)
        queue.append(lnk)
    return queue
url='http://tieba.baidu.com/p/1569069059'
def unique(queue):#queue里面全是队列
    visited=set()#定义一个集合
    for i in range(len(queue)):
        print(i,"这是queue中的url",queue[i])
unique(catchhref(url))