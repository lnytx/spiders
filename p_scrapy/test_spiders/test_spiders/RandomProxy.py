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
from twisted.web._newclient import ResponseNeverReceived


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
class HttpProxyMiddleware(object):
    '''
    https://github.com/kohn/HttpProxyMiddleware/blob/master/fetch_free_proxyes.py
    '''
    # 遇到这些类型的错误直接当做代理不可用处理掉, 不再传给retrymiddleware
    def __init__(self):
    # 是否在超时的情况下禁用代理
        self.invalid_proxy_flag = True
        DONT_RETRY_ERRORS = (TimeoutError, ConnectionRefusedError, ResponseNeverReceived, ConnectError, ValueError)
        self.proxyList = []
    #     f_ip = "D:\\Program Files\\Python_Workspace\\spiders\\p_scrapy\\test_spiders\\test_spiders\\proxy_ip.txt"
        self.f_ip = "E:\\soft\\python3.4\\workspace\\spiders\\p_scrapy\\jiayuan\\jiayuan\\proxy_ip.txt"
        with open (self.f_ip,'r') as f:
            for line in f.readlines():
                print("line",line)
                self.proxyList.append(line)
#     proxyList = ["122.114.31.177:808"]
    def process_request(self, request, spider):  
        # Set the location of the proxy  
        pro_adr = random.choice(self.proxyList)  
        print("当前使用的代理IP:" + pro_adr)  
        request.meta['proxy'] = "http://" + pro_adr  
    def process_exception(self, request, exception, spider):
        """
            处理由于使用代理导致的连接异常
        """
#         request_proxy_index = request.meta["proxy_index"]
        print('Failed to request url %s w with exception %s' % (request.url, str(exception)))
        print("出现异常",str(exception))
        # 只有当proxy_index>fixed_proxy-1时才进行比较, 这样能保证至少本地直连是存在的.
        if isinstance(exception, HttpError):
            print("出现异常",str(exception))
#             if request_proxy_index > self.fixed_proxy - 1 and self.invalid_proxy_flag: # WARNING 直连时超时的话换个代理还是重试? 这是策略问题
#                 if self.proxyes[request_proxy_index]["count"] < self.invalid_proxy_threshold:
#                     self.invalid_proxy(request_proxy_index)
#                 elif request_proxy_index == self.proxy_index:  # 虽然超时，但是如果之前一直很好用，也不设为invalid
#                     self.inc_proxy_index()
            with open (self.f_ip,'r') as f:
                for line in f.readlines():
                    print("line",line)
                    self.proxyList.append(line)
            pro_adr = random.choice(self.proxyList)  
            print("换一个代理IP:" + pro_adr)  
            request.meta['proxy'] = "http://" + pro_adr  
            return request

