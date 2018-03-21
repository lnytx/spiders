# -*- coding: utf-8 -*-
'''
Created on 2018年3月1日

@author: ning.lin
添加随机的一些useragent
'''
import random

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

from jiayuan.settings import USER_AGENT_LIST


class UserAgent(UserAgentMiddleware):
    def __init__(self, user_agent=''):  
        self.user_agent = USER_AGENT_LIST
    def process_request(self, request, spider):  
        ua = random.choice(self.user_agent)  
        if ua:  
            #显示当前使用的useragent  
            #print "********Current UserAgent:%s************" %ua  
            #记录 
            print("当前使用的agent",ua) 
#             print("当前的url",request.url)
            request.headers.setdefault('User-Agent', ua)  