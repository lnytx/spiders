# -*- coding: utf-8 -*-
'''
Created on 2018年3月1日

@author: ning.lin
设置代理IP
'''
import random



class ProxyIP(object): 
    proxyList = []
#     f_ip = "D:\\Program Files\\Python_Workspace\\spiders\\p_scrapy\\test_spiders\\test_spiders\\proxy_ip.txt"
    f_ip = "E:\\soft\\python3.4\\workspace\\spiders\\p_scrapy\\jiayuan\\jiayuan\\proxy_ip.txt"
    with open (f_ip,'r') as f:
        for line in f.readlines():
            print("line",line)
            proxyList.append(line)
    def process_request(self, request, spider):  
        # Set the location of the proxy  
        pro_adr = random.choice(self.proxyList)  
        print("当前使用的代理IP:" + pro_adr)  
        request.meta['proxy'] = "http://" + pro_adr  
