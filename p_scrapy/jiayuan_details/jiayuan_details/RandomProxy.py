# -*- coding: utf-8 -*-
'''
Created on 2018年3月1日

@author: ning.lin
设置代理IP
'''
import random




class ProxyIP(object): 
    proxyList = ["47.52.222.165:80"]
    def process_request(self, request, spider):  
        # Set the location of the proxy  
        pro_adr = random.choice(self.proxyList)  
        print("当前使用的代理IP:" + pro_adr)  
        request.meta['proxy'] = "http://" + pro_adr  
