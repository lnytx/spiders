# -*- coding:utf-8 -*-
'''
Created on 2018年2月28日
@author: ning.lin
'''
'''
大图地址class或id有big字样 的
<div class="pho_big" id="phoBig" style="height: 640px;">
<div class="big_pic fn-clear" id="bigImg">
小图地址
<div class="pho_small_box fn-clear mt25 " id="phoSmallPic">
'''

import json
import time

from apscheduler.util import xrange
import requests
from scrapy  import log
from scrapy import cmdline
import scrapy
from scrapy.http import Request
from scrapy.http.request.form import FormRequest
from scrapy_redis.spiders import RedisSpider
from selenium import webdriver



class jiayuan_data(RedisSpider):
    name = "details"
    redis_key = 'jiayuan_main:start_urls'
    login_url = 'http://login.jiayuan.com/'#登录时的url
    url_base = 'http://www.jiayuan.com/89257310?m_type=11&chat=1&ol=1&flt=zdlook1_demonil&fxly=tj-yxtj-xntc'
    redis_key = "sinaspider:strat_urls"
    start_urls = []
    pre_page_num = 25#每个搜索业面有25条记录
    #print("start_urls",len(start_urls))
#     start_urls = [
#         "http://search.jiayuan.com/v2/search_v2.php",#直接搜索结果，获取个人主页的url(先不登录)
        #"https://passport.jiayuan.com/dologin.php?pre_url=http://www.jiayuan.com/usercp",#登录页面post数据
#     ]
    '''
        下载器中间件在下载器和Scrapy引擎之间，每一个request和response都会通过中间件进行处理。
        在中间件中，对request进行处理的函数是process_request(request, spider)
    '''
    def start_requests(self):#
        print("执行start_requestsstart_requestsstart_requests")
        yield scrapy.Request(url=self.login_url, callback=self.get_main_info)
#             yield scrapy.Request(url=search_url,callback=self.get_main_info)
            #yield Request(url=url,meta={'cookiejar':1},callback=self.get_count_info)
    
#     def login(self, response):
#         _s_x_id = response.xpath("//input[@name='_s_x_id']/@value").extract_first()
#         print("_s_x_id的值",_s_x_id)
#         if _s_x_id is None:
#             return ''
#         post_data = {
#             "name":"这是我的用户名",
#             "password":"*******************",
#             "remem_pass":"on",
#             "_s_x_id":_s_x_id,
#             "ljg_login":"1",
#             "m_p_l":"1",
#             "channel":"0",
#             "position":"0"
#         }
#         Cookie1 = response.headers.getlist('Set-Cookie')   #查看一下响应Cookie，也就是第一次访问注册页面时后台写入浏览器的Cookie
#         print("Cookie1的值",Cookie1)
#         
#         cookies = json.dumps(Cookie1)
#         print('登录中')
#         return  scrapy.FormRequest.from_response(response,
#                                           url=self.url_base,   #真实post地址
#                                           formdata=post_data,
#                                           dont_filter=True,
#                                           callback=self.get_main_info
#                                           )
    
    def get_main_info(self,response):
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        option.add_argument("--window-size=1920,1080")
          
        driver = webdriver.Chrome(chrome_options=option)
        driver = webdriver.Chrome()
        driver.get(self.login_url)#登录
        driver.implicitly_wait(2)
        time.sleep(3)
        driver.find_element_by_id("login_btn").click()
        driver.find_element_by_id("login_email").clear()
        driver.find_element_by_id("login_email").send_keys("这是我的用户名") #修改为自己的用户名
        driver.find_element_by_id("login_password").clear()
        driver.find_element_by_id("login_password").send_keys("*******************") #修改为自己的密码
#         #登录url
#         #url="http://login.jiayuan.com/"
        driver.find_element_by_id("login_btn").click()#点击登录按钮
        cookies = driver.get_cookies()#获取cookies
        
        print("response.response的值.url",response.url)
#         driver.get(response.url)
        time.sleep(3)
        print("next的 值",response.url)
        #body = response.body
        #print("网岩浆值",body)
        info = response.body.decode("utf-8")   #登录后可以查看一下登录响应信息json.loads(
        #print("info",info)
        print('打开浏览器')
        print("当前的url",response.url)
        
        #跳到指定详情业面
        driver.get(self.url_base)
        
        print("整个页面",driver.page_source)
        #print(driver.title)
        #driver.save_screenshot('登录时.png')
#             get_chrome_less(driver,search_url,p)#登录并滚动到最下方
        #find_element_by_tag_name('div').text
        #user_list = response.xpath('/html//ul[@id="normal_user_container"]').extract()使用reponse时为空，因为没有用driver加载url
#         address = ','.join(response.xpath('/html//h6[@class="member_name"]/a/text()').extract())#得到多个a标签的text
#         person_info = response.xpath('/html//ul[@class="member_info_list fn-clear"]/li')#xpathy方式获取元素
        address = driver.find_elements_by_xpath('/html//h6[@class="member_name"]/a')#得到多个a标签的text
        str_address=''
        for item in address:
            str_address += item.get_attribute("text") 
        print("人员地址",str_address)
        person_info = driver.find_elements_by_xpath('/html//ul[@class="member_info_list fn-clear"]/li')
        print("人员主信息",type(person_info),person_info)
        print("person_info[2]第3条记录",person_info[2])
        #webdriver获取值
        buy_car = person_info[2].find_element_by_xpath('div[@class="fl f_gray_999"]').get_attribute("text")
        print("buy_car的属性 ",type(buy_car),buy_car)
        print("是否购车",buy_car)
        buy_car_info = person_info[2].find_element_by_xpath('div[@class="fl pr"]/em').text
        #buy_car = person_info[2].xpath('div/text()').extract()[0]
        #buy_car_info = person_info[2].xpath('div/em/text()').extract()
        
        #xpath方法获取item值
#         buy_car = person_info[2].xpath('div[@class="fl f_gray_999"]/text()').extract()[0]
#         buy_car_info = person_info[2].xpath('div[@class="fl f_gray_999"]//em/text()')
#         buy_car_info = person_info[2].xpath('div[@class="fl pr"]//em/text()')
        
        print("是否购车",buy_car_info)#未登录时这里是空的
        time.sleep(10000)
        #print("user_list",type(user_list),user_list)
        
        
