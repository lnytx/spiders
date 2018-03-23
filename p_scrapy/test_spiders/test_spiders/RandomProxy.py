# -*- coding: utf-8 -*-
'''
Created on 2018年3月1日

@author: ning.lin
设置代理IP
'''
import random

from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import ConnectError



#定义几个全局变量

import datetime
import random
import time

import pymysql

'''
从http://www.xicidaili.com/获取代理IP，并验证是否能访问爬虫目标网站
如果不能访问，则删除，
'''
#定义几个全局变量

from distutils.command.check import check
from multiprocessing import Pool
import multiprocessing
import os
from queue import Queue
import random
import re
import socket
import threading
import time

from bs4 import BeautifulSoup
import pymysql
import requests
from scrapy.utils.project import get_project_settings


def connect():
    config={'host':'127.0.0.1',
                'user':'root',
                'password':'root',
                'port':3306,
                'database':'jiayuan',
                'charset':'utf8',
                #要加上下面一行返回的是list，否则默认返回的是tuple
                'cursorclass':pymysql.cursors.DictCursor,
            }
    try:
        conn=pymysql.connect(**config)
        print("conn is success!")
        return conn
    except Exception as e:
        print("conn is fails{}".format(e))



'''
获取网上的代理IP
'''
settings = get_project_settings()


print("文件为",settings['PROXY_IP_FILE'])
PROXY_IP_FILE=settings['PROXY_IP_FILE']


lock = threading.Lock()#定义锁，防止重复写文件
q = Queue()#创建先进先出队列，全局中变量
if os.path.exists(PROXY_IP_FILE+'_temp'):
    pass
else:
    temp = open(PROXY_IP_FILE+'_temp','a+')
    temp.close()
if os.path.exists(PROXY_IP_FILE):
    pass
else:
    temp = open(PROXY_IP_FILE,'a+')
    temp.close()
r_fine = open(PROXY_IP_FILE+'_temp')
w_file = open(PROXY_IP_FILE,'a+')#IP写入正式文件




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
    global q
    ip_list={}   #初始化列表用来存储获取到的IP
#     url='http://www.xicidaili.com/'
    url = "http://ip.yqie.com/ipproxy.htm"
#     url = "http://ip.seofangfa.com/"
    req=requests.get(url=url,headers=header)
    r=req.text
    soup=BeautifulSoup(r,'html.parser')
#     print("soup",soup)
#     iplistn=soup.findAll('tr',class_='')#对应的url='http://www.xicidaili.com/'
    iplistn=soup.findAll('tr',align='center')#url = "http://ip.yqie.com/ipproxy.htm"
#     print("iplistn",iplistn)
    proxy_ip=[]
    set_ip = set()#利用set去除文件中重复的IP
    ip_port=''
    for i in iplistn:
        ip=i.text.strip().strip()
        ip_list=ip.split()
        for j in range(len(ip_list)):
            p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')#判断是否为IP
            if p.match(ip_list[j]):#如果是IP
                #ip_port[ip_list[j]]=ip_list[j+1]
                ip_port = str(ip_list[j].strip())+":"+str(ip_list[j+1].strip())#119.188.94.145:80这种形式
                set_ip.add(ip_port)
#                 print("ip_port",ip_port)
    with open(PROXY_IP_FILE+'_temp','a+') as f:
        for name in set_ip:
            q.put(ip_port)#遍历set，将其元素添加到队列中
            file_ip = str(str(name))+'\n'
            f.write(file_ip)   

#     print("lifo_queue",q.queue)
#     print("获取第一个元素",q.get())
    return q
#使用代理IP访问url




def check_url():
    '''
    deque['119.188.94.145:80', '113.120.130.249:8080']
    url为网站url,验证上面获取的IP是否能用
    '''
#     que = get_proxyIP()
    user_agent_list = [\
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
    #根据上面的方法获取一个随机的代理IP
    #q=get_proxyIP()
    url = "http://www.jiayuan.com/175017527?fxly=pmtq-ss-210&pv.mark=s_p_c|175017527|68209968"
    ip={}
    req = ''
    #获取数据连接
    conn=connect()
    cursor=conn.cursor()
    
    while True:
        lock.acquire()
        ip["http"] = r_fine.readline().strip()#读取文件中的一行
#         ip['http'] = que.get()#从队列中读取爬到的IP
        lock.release()#释放锁
        if  len(ip["http"]) == 0: break#到了文件结尾就清空则停止
        print("当前验证的IP:",ip)
        try:
            req = requests.get(url, proxies=ip, headers=header)
            print("返回状态码",req.status_code)
#             if req.status_code!=200:
#                 continue
            if req.status_code==200:
                print("写入文件")
                lock.acquire()#加锁写文件
                for k,v in ip.items():
                    file_ip = str(str(v))+'\n'
                    print("状态为200的IP:",file_ip)
                    w_file.write(file_ip)
                    '''
                                    并且写入数据库中
                    '''
                    try:
                        cursor.execute("select ip_port from proxy_ip where ip_port=%s",(str(v).strip()))
                        ip_exit = cursor.fetchone()
                        print("ip_exit",ip_exit)
                        if ip_exit:
                            print("执行updata")
                            cursor.execute('''update proxy_ip set proxy_ip=%s,user_agent=%s where ip_port=%s''',(str(v).strip(),str(random.choice(user_agent_list)),str(v).strip()))
                        else:
                            print("执行insert")
                            cursor.execute("insert into proxy_ip(ip_port,user_agent) value(%s,%s)",(str(v).strip()),str(random.choice(user_agent_list)))
                    except Exception as e:
                        print("执行sql异常",str(e))
                    finally:
                        conn.commit()
                lock.release()#释放锁218.56.132.154:8080,159.255.163.189:80
            else:#等于200将当前IP写入文本中
                continue
#             r=req.text
#             soup=BeautifulSoup(r,'html.parser')
        except Exception as e:
            print("异常",str(e))
        finally:
            pass
    #去掉IP中的回车与换行
    cursor.execute('''SELECT ip_port FROM proxy_ip WHERE id >= \
                        ((SELECT MAX(id) FROM proxy_ip)-(SELECT MIN(id ) \
                        FROM proxy_ip)) * RAND() + (SELECT MIN(id) FROM proxy_ip)  LIMIT 1)
                ''')
    curr_ip = cursor.fetchone()['ip_port']
    cursor.execute("UPDATE proxy_ip SET  ip_port = REPLACE(REPLACE(ip_port, CHAR(10), ''), CHAR(13), '')")
    #scrapy代理会始终获取状态为1的IP做为代理IP，直到超时或使用了1个小时,初始时数据库中始终有一个状态为1的IP
    cursor.execute("update proxy_ip SET is_current=1 where ip_port=%s",curr_ip)
    conn.commit()
    conn.close()
    #随机将其中一条数据的当前状态入为0
            #如果不是200就重试，每次递减重试次数,使用函数获取soup数据
                #如果url不存在会抛出ConnectionError错误，这个情况不做重试  
            #return check_url(url,retry-1)
                #req.close()
#当前IP {'http': '42.96.168.79:8888'}
      
#利用set去掉重复的行
def filter_file():
    set_line = set()
    if os.path.exists(PROXY_IP_FILE+'_temp'):
        with open(PROXY_IP_FILE+'_temp','r') as f:
            for line in f.readlines():
                print("line",line)
                set_line.add(line)
        print(type(set_line),type)
        with open(PROXY_IP_FILE,'a+') as f:
            for item in set_line:
                print("item",item)
                f.write(item)

def main():
    get_proxyIP()#获取IP，写入临时文件
    
    '''
    多线程
    '''
    thread_list = []    #线程存放列表
    for i in range(40):
        t =threading.Thread(target=check_url,args=())
        t.setDaemon(True)
        thread_list.append(t)
        
    for t in thread_list:
        t.start()
        
    for t in thread_list:
        t.join() 





'''
在中间件中获取代理IP
'''
def get_random_ip(change_ip=0):
    conn=connect()
    cursor=conn.cursor()
    now_time = time.strftime("%Y-%m-%d %H:%M:%S")
    if change_ip==0:#未传入change_ip说明是爬虫第一次开始，默认随机获取IP，不是更改IP
        try:
            rand_ip_slq = '''SELECT ip_port,user_agent FROM proxy_ip WHERE id >= \
                        ((SELECT MAX(id) FROM proxy_ip)-(SELECT MIN(id ) \
                        FROM proxy_ip)) * RAND() + (SELECT MIN(id) FROM proxy_ip)  LIMIT 1
            '''
            cursor.execute(rand_ip_slq)
            ip_exit = cursor.fetchone()
            print("ip_exit",ip_exit)
            if ip_exit:
               #将当前获取的IPcurrent状态改为1并且修改当前时间为最近一次使用时间
                cursor.execute('''update proxy_ip set is_current=%s,last_time_use=%s where ip_port=%s''',(1,now_time,ip_exit['ip_port']))
            else:
                print("未找到sql该表可能为空，需要去爬IP")
                main()#从网上获取IP并写入数据库中
        except Exception as e:
            print("执行sql异常",str(e))
        finally:
            conn.commit()
            conn.close()
    else:#更改代理IP
        try:
            rand_ip_slq = '''SELECT ip_port FROM proxy_ip WHERE id >= \
                        ((SELECT MAX(id) FROM proxy_ip)-(SELECT MIN(id ) \
                        FROM proxy_ip)) * RAND() + (SELECT MIN(id) FROM proxy_ip)  LIMIT 1
                        '''
            cursor.execute(rand_ip_slq)
            ip_exit = cursor.fetchone()
            print("ip_exit2",ip_exit)
            if ip_exit:
               #将当前获取的IPcurrent状态改为1表示当前在使用的IP并且修改当前时间为最近一次使用时间
                cursor.execute('''update proxy_ip set is_current=%s,last_time_use=%s where ip_port=%s''',(1,now_time,ip_exit['ip_port']))
                #将之前状态为当前IP的状态改成0（非当前IP）
                cursor.execute("select last_time_use from proxy_ip where ip_port=%s",change_ip)
                use_time = cursor.fetchone()['last_time_use']
                startTime= datetime.datetime.strptime(str(use_time),"%Y-%m-%d %H:%M:%S")  
                endTime= datetime.datetime.strptime(str(now_time),"%Y-%m-%d %H:%M:%S")
                seconds = (endTime- startTime).seconds#获取此次与上次时间之差就等于使用了的时间
                cursor.execute('''update proxy_ip set is_current=%s,use_times=%s where ip_port=%s''',(0,seconds,change_ip))
                #cursor.execute('''update proxy_ip set is_current=%s,last_time_use=%s where ip_port=%s''',(1,now_time,ip_exit['ip_port']))
            else:
                print("未找到sql该表可能为空，需要去爬IP")
#                 main()#从网上获取IP并写入数据库中
        except Exception as e:
            print("未找到sql该表可能为空，需要去爬IP",str(e))
#             main()#从网上获
        finally:
            conn.commit()
            conn.close()
    return ip_exit#返回格式165.227.40.248:3128
        
def get_proxy_ip():
    '''
    scrapy通过些函数获取is_current状态为1的IP为代理IP，防止一次request换一次IP（因为登录情况下不可能出现这种情况）
    '''
    conn=connect()
    cursor=conn.cursor()
    try:
        cursor.execute("select ip_port from proxy_ip where is_current=1")
        pro_ip = cursor.fetchone()['ip_port']
    except Exception as e:
        print("get_proxy_ip报错",str(e))
    finally:
            conn.commit()
            conn.close()
    return pro_ip

# class ProxyIP(object): 
#     proxyList = []
#     f_ip = "D:\\Program Files\\Python_Workspace\\spiders\\p_scrapy\\test_spiders\\test_spiders\\proxy_ip.txt"
#     with open (f_ip,'r') as f:
#         for line in f.readlines():
#             print("line",line)
#             proxyList.append(line)
# #     proxyList = ["122.114.31.177:808"]
#     def process_request(self, request, spider):  
#         # Set the location of the proxy  
#         pro_adr = random.choice(self.proxyList)  
#         print("当前使用的代理IP:" + pro_adr)  
#         request.meta['proxy'] = "http://" + pro_adr  
#RetryMiddleware
'''
代理中间件
'''
class ProxyIP(object):
    '''
    https://github.com/kohn/HttpProxyMiddleware/blob/master/fetch_free_proxyes.py
    '''
    # 遇到这些类型的错误直接当做代理不可用处理掉, 不再传给retrymiddleware
    def __init__(self):
    # 是否在超时的情况下禁用代理
#     proxyList = ["122.114.31.177:808"]
        self.proxy_ip = get_proxy_ip()
    def process_request(self, request, spider):  
        # Set the location of the proxy  
        print("当前使用的代理IP:" + self.proxy_ip)  
        request.meta['proxy'] = "http://" + self.proxy_ip  
    def process_exception(self, request, exception, spider):
        """
            处理由于使用代理导致的连接异常
        """
#         request_proxy_index = request.meta["proxy_index"]
        print('Failed to request url %s w with exception %s' % (request.url, str(exception)))
        # 只有当proxy_index>fixed_proxy-1时才进行比较, 这样能保证至少本地直连是存在的.
        print("出现异常",str(exception))
#             if request_proxy_index > self.fixed_proxy - 1 and self.invalid_proxy_flag: # WARNING 直连时超时的话换个代理还是重试? 这是策略问题
#                 if self.proxyes[request_proxy_index]["count"] < self.invalid_proxy_threshold:
#                     self.invalid_proxy(request_proxy_index)
#                 elif request_proxy_index == self.proxy_index:  # 虽然超时，但是如果之前一直很好用，也不设为invalid
#                     self.inc_proxy_index()
        proxy_ip = get_random_ip(self.proxy_ip)
        print("换一个代理IP:" + proxy_ip)
        request.meta['proxy'] = "http://" + proxy_ip
#         return request



