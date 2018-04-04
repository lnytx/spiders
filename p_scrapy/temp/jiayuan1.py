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
    name = "testa"
    allowed_domains = ["jiayuan.com"]
    start_urls = (
        'http://login.jiayuan.com/',
    )

    def get_cookies(self):
        driver = webdriver.Chrome()
        driver.get(self.start_urls[0])
        driver.find_element_by_id("login_btn").click()
        driver.find_element_by_id("login_email").clear()
        driver.find_element_by_id("login_email").send_keys("这是我的用户名") #修改为自己的用户名
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
        print("123123")
        login_url = 'http://login.jiayuan.com/'  # 登录页面
        return [scrapy.Request(url=login_url,meta={'cookiejar':1},callback=self.login)]
    
    def login(self, response):#模拟登录
        _s_x_id = response.xpath("//input[@name='_s_x_id']/@value").extract_first()
        print("_s_x_id的值",_s_x_id)
        if _s_x_id is None:
            return ''
        post_url = 'https://passport.jiayuan.com/dologin.php?pre_url=http://www.jiayuan.com/usercp'    # 这里是输入手机号
        post_data = {
            "name":"这是我的用户名",
            "password":"*******************",
            "remem_pass":"on",
            "_s_x_id":_s_x_id,
            "ljg_login":"1",
            "m_p_l":"1",
            "channel":"0",
            "position":"0"
        }
        Cookie1 = response.headers.getlist('Set-Cookie')   #查看一下响应Cookie，也就是第一次访问注册页面时后台写入浏览器的Cookie
        print("Cookie1的值",Cookie1)
        print('登录中')
        return  scrapy.FormRequest.from_response(response,
                                          url=post_url,   #真实post地址
                                          meta={'cookiejar':response.meta['cookiejar']},
                                          formdata=post_data,
                                          dont_filter=True,
                                          callback=self.next
                                          )
    
    def next(self,response):
        print("response的 值",response)
        #a = response.body.decode("utf-8")   #登录后可以查看一下登录响应信息
        #print("剑灵后的body",a)
        #print("response.bodyresponse.body",response.body)
        title = response.xpath('/html/head/title/text()').extract()
        print("登录后的title",title)
        my_url = "http://www.jiayuan.com/usercp/?from=login"
        #yield scrapy.FormRequest(url=my_url, callback=self.parse)
        #查取所有女性数据，去掉地区，年龄，身高等手动点击处理掉
        search_url = "http://search.jiayuan.com/v2/index.php?key=&sex=f&stc=&sn=default&sv=1&p=1&pt=56114&ft=off&f=select&mt=d"
        yield scrapy.Request(url=search_url, callback=self.parse)
        #yield scrapy.Request(url=my_url,callback=self.pase)
        """登录后请求需要登录才能查看的页面，如个人中心，携带授权后的Cookie请求"""
        #yield Request('http://edu.iqianyue.com/index_user_index.html',meta={'cookiejar':True},callback=self.next2)
    
    def parse(self,response):
        print("获取个人主页jiayuan")
        print("执行parse函数",response)
        title = response.xpath('/html/head/title/text()').extract()[0]
        print("登录后的title",title)
        #a = response.body.decode("utf-8")
        #print("页面%s"%(response.url),response.text)
        #已经登录了，使用浏览器打开
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
            
    
cmdline.execute("scrapy crawl jiayuan".split())