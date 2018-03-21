# -*- coding:utf-8 -*-
'''
Created on 2018年2月28日
@author: ning.lin
'''

import json

from scrapy import cmdline
import scrapy
from selenium import webdriver


class ZhihuSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["jiayuan.com"]
    start_urls = (
        'http://login.jiayuan.com/',
    )

    def get_cookies(self):
        driver = webdriver.Chrome()
        driver.get(self.start_urls[0])
        driver.find_element_by_id("login_btn").click()
        driver.find_element_by_id("login_email").clear()
        driver.find_element_by_id("login_email").send_keys("lnytx@163.com") #修改为自己的用户名
        driver.find_element_by_id("login_password").clear()
        driver.find_element_by_id("login_password").send_keys("*******************") #修改为自己的密码
        #登录url
        #url="http://login.jiayuan.com/"
        driver.find_element_by_id("login_btn").click()#点击登录按钮
        cookies = driver.get_cookies()
        driver.close()
        print ("cookies",cookies)
        return cookies
    
    def start_requests(self):#
        print("start_requests")
        cookies = self.get_cookies()
        search_url = 'http://search.jiayuan.com/v2/index.php?key=&sex=f&stc=&sn=default&sv=1&p=1&pt=56453&ft=off&f=select&mt=d'  # 登录页面
        return [scrapy.Request(url=search_url,cookies=cookies,callback=self.parse)]
    
    
    
    def parse(self,response):
        print("获取个人主页11111111111")
        print("执行parse函数",response)
        title = response.xpath('/html/head/title/text()').extract()
        print("登录后的title",title)
        a = response.body.decode("utf-8")
        print("页面",a)
        #已经登录了，使用浏览器打开
        driver = webdriver.Chrome()
        driver.get("search_url = 'http://search.jiayuan.com/v2/index.php?key=&sex=f&stc=&sn=default&sv=1&p=1&pt=56453&ft=off&f=select&mt=d'")
        
        
        current_url = response.url #爬取时请求的url
        body = response.body  #返回的html
        #unicode_body = response.body_as_unicode()#返回的html unicode编码
        string = response.text
        #print("查询的主页",string)
        #user_list = response.xpath('/html//ul[@id="normal_user_container"]').extract()
        user_list = response.xpath('//div[contains(@class,"search_userHead")]')
        print("人员列表user_list",type(user_list),user_list)
        #a[last()]/@href'
        for item in user_list:
            pass
            #print("人员列表",type(item),item)
            
    
cmdline.execute("scrapy crawl test".split())