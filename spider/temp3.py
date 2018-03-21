'''
Created on 2017��4��10��

@author: ning.lin
'''
#��վ�����棺һ��IPƵ�����ʾ��Ƚ���IP���������
#��������ԣ�����IP����Ƶ�ʣ�����Ƶ�ʾ��Զ��Ͽ�������������ٶȣ���ÿ������ǰ��time.sleep,�����IP
#���Զ�����̨�Է��ʽ���ͳ�ƣ��������userAgent���ʳ�����ֵ�����Է��������˽ϴ�һ����վ��ʹ��
#�����������cookies��һ����վ��ʹ��

import urllib.request
import re
import random
import time

#���ȣ�������һ����������IP����վ���Ӹ���վ��ȡ����IP��������ҳ��������IPʧЧ�����ô���IP

class download(object):
    def __init__(self):
        self.ip_list=[]   #��ʼ���б������洢��ȡ����IP
        html=urllib.request.Request("http://haoip.cc/tiqu.htm")
        iplistn=re.findall(r'r/>(.*?)<b',html.text,re.S)   #��html�����л�ȡ����/><b�е����� re.S����˼��ƥ��������л��з�
        for ip in iplistn:
            i=re.sub("\n","",ip)    #re.sub��reģ���滻�ķ��������ʾ��\n�滻Ϊ��
            self.ip_list.append(i.strip())   #��IP��ӵ���ʼ���б���

        self.user_agent_list=[
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
    def get(self,url,timeout,proxy=None,num_retries=6):
        ua=random.choice(self.user_agent_list)   #��user_agent_list�������ȡ��һ���ַ���
        # print(ua)
        header={"User-Agent":ua}  #����һ��������User_Agent

        if proxy==None:    #������Ϊ��ʱ����ʹ�ô����ȡresponse
            try:
                response=urllib.request.Request(url,headers=header,timeout=timeout)
                return response
            except:
                if num_retries>0:
                    time.sleep(10)
                    print(u"��ȡ��ҳ����10s�󽫻�ȡ�����ڣ�",num_retries,u"��")
                    return self.get(url,timeout,num_retries-1)  #����������������1
                else:
                    print(u"��ʼʹ�ô���")
                    time.sleep(10)
                    IP="".join(str(random.choice(self.ip_list)).strip())
                    proxy={"http":IP}
                    return self.get(url,timeout,proxy)

        else:
            try:
                IP="".join(str(random.choice(self.ip_list)).strip())   #���ȡIP��ȥ���ո�
                proxy={"http":IP}   #����һ������
                response=urllib.request.Request(url,headers=header,proxies=proxy,timeout=timeout)  #ʹ�ô�������ȡresponse
                return response
            except:
                if num_retries>0:
                    time.sleep(10)
                    IP="".join(str(random.choice(self.ip_list)).strip())
                    print(u"���ڸ�������10s�����»�ȡ��",num_retries,u"��")
                    print(u"��ǰ�����ǣ�",proxy)
                    return self.get(url,timeout,proxy,num_retries-1)
                else:
                    print(u"����������ȡ������")
                    return self.get(url,3)

request=download();