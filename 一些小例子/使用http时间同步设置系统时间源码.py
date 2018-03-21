'''
Created on 2017年5月9日

@author: ning.lin
'''
from http import client
import os
import time
import dateutil.parser as dateparser

def getBeijinTime():
    try:
        conn = client.HTTPConnection("www.baidu.com")
        conn.request("GET", "/")
        response = conn.getresponse()
        print("response",response)
        data=response.getheader('date')
        print("data",data)
        print (response.status, response.reason)
        dt = dateparser.parse(data)
        # OR: dt = time.strptime(datetimestring, fmt)
        s=time.mktime(dt.timetuple())
        print("str----->timestamp",s)
        fmt='%Y-%m-%d %H:%M:%S'
        x = time.localtime(s+8*60*60)
        date1=time.strftime(fmt,x)
        print("从网站取得的北京时间",date1)
        return date1
    except:
        return None
if __name__=='__main__':
    print("aaa",getBeijinTime())