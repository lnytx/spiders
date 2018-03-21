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

from jiayuan_details.items import JiayuanItem,PersonInfo


class jiayuan_data(RedisSpider):
    name = "jiayuan_slave"
    redis_key = 'jiayuan_main:start_urls'
    url_base = 'http://search.jiayuan.com/v2/index.php?key=&sex=f&stc=&sn=default&sv=1&p=%s&pt=153649&ft=off&f=select&mt=d'
    redis_key = "sinaspider:strat_urls"
    login_url = 'http://login.jiayuan.com/'#登录时的url
    start_urls = []
    pre_page_num = 25#每个搜索业面有25条记录
    #head less模拟登录
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(chrome_options=option)
    driver.get(login_url)
    time.sleep(3)
    driver.find_element_by_id("login_btn").click()
    driver.find_element_by_id("login_email").clear()
    driver.find_element_by_id("login_email").send_keys("lnytx@163.com") #修改为自己的用户名
    driver.find_element_by_id("login_password").clear()
    driver.find_element_by_id("login_password").send_keys("************") #修改为自己的密码
    #登录url
    #url="http://login.jiayuan.com/"
    driver.find_element_by_id("login_btn").click()#点击登录按钮
    cookies = driver.get_cookies()#获取cookies
    for p in range(1,153649):
        search_url = "http://search.jiayuan.com/v2/index.php?key=&sex=f&stc=&sn=default&sv=1&p=%s&pt=%s&ft=off&f=select&mt=d" %(p,153649)
        start_urls.append(search_url)
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
        for url in self.start_urls:
            yield scrapy.Request(url=url,cookies=self.cookies,callback=self.get_main_info)
#             yield scrapy.Request(url=search_url,callback=self.get_main_info)
            #yield Request(url=url,meta={'cookiejar':1},callback=self.get_count_info)
    def get_main_info(self,response):#解析搜索业面的url
        print("next的 值",response.url)
        #body = response.body
        #print("网岩浆值",body)
        info = response.body.decode("utf-8")   #登录后可以查看一下登录响应信息json.loads(
#         print("登录后的body",info)#直接使用这里面的href也可以登录
#         print("总的页数",info['pageTotal'])
#         print("总的人数",info['count'])
#         print("是否登录",info['isLogin'])
#         print("当前userinfo个数",len(info['userInfo']))
#         print("获取个人主页jiayuan",response)
#         result = response.meta['result']
        #获取搜索页面的人员主要item
        self.driver.get(response.url)
        self.driver.implicitly_wait(3)
        page_count=0
        for url in self.start_urls:
            time.sleep(1) 
            print("当前的url",url)
            print('重新加载url')
            #print(driver.title)
            #driver.save_screenshot('登录时.png')
#             get_chrome_less(driver,search_url,p)#登录并滚动到最下方
#             print("page_count页面",self.driver.page_source)
            #find_element_by_tag_name('div').text
            #user_list = response.xpath('/html//ul[@id="normal_user_container"]').extract()使用reponse时为空，因为没有用driver加载url
            user_list = self.driver.find_elements_by_xpath('/html//ul[@id="normal_user_container"]/li')#得到多个li标签
            #print("user_list",user_list)
            if user_list==[]:
                print("下一页")
            #print("user_list",type(user_list),user_list)
            item = JiayuanItem()
            person_count=0
            url_details = []#详情页面的url
            for user in user_list:
                person_count+=1
                print("第%s个人",person_count)
                #获取个人主页入口及昵称
                url_info = user.find_elements_by_xpath('//div[@class="hy_box"]//div[@class="user_name"]/a[@class="os_stat"]')
                #print("一次输出结题",url_info)
#                 user_info = item.find_elements_by_xpath('//div[@class="hy_box"]/p[@class="user_info"]')
#                 heigth_info = item.find_elements_by_xpath('//div[@class="hy_box"]/p[@class="zhufang"]/span')
                #.find_elements_by_tagName('span')
                for url in url_info:#通过url去获取别的信息
                #print("人员主页的url",item.find_elements_by_xpath)
                    try:
                        print("人员主页url",type(url),url)
#                         person_id =  url[url.rfind('/')+1:url.index('?')]
                        print("昵称",url.get_attribute("text"))
                        ss=url.find_element_by_xpath('../../p[@class="user_info"]')
                        print("年龄_城市",ss.text,type(ss))
                        hhs=url.find_element_by_xpath('../../p[@class="zhufang"]').find_elements_by_tag_name('span')
                        temp_str = ''
                        for hh in hhs:
                            print("身高元素",hhs)
                            temp_str = hh.text+'_'+temp_str
                            print("temp_strtemp_str",temp_str)
                        print("合并",temp_str)
                        item['heigth'] = temp_str[:-1]#去掉最后一个下划线
                        item['user_info'] = ss.text
                        item['nick_name'] = url.get_attribute("text")
                        item['main_url'] = url.get_attribute("href")
                        print("人员主页url",type(url),url.get_attribute("href"))
                        person_id =  item['main_url'][item['main_url'].rfind('/')+1:item['main_url'].index('?')]
                        print("人员唯一的ID",person_id)
                        item['person_id'] = person_id
                        url_details.append(item['main_url'])
                        print("身高",item['heigth'])
                        if url_details!=[]:
                            for url in url_details:
                                yield scrapy.Request(url=url,cookies=self.cookies,callback=self.get_details)
                        yield item
                    except Exception as e:
                        raise  Exception(str(e))
    def get_details(self,response):
        item = PersonInfo()
        person_id =  response.url[response.url.rfind('/')+1:response.url.index('?')]
        print("response.response的值.url",response.url)
#         driver.get(response.url)
        time.sleep(3)
        print("人员详情页面",response.url)
        #body = response.body
        #print("网岩浆值",body)
        info = response.body.decode("utf-8")   #登录后可以查看一下登录响应信息json.loads(
        #print("info",info)
        print('打开浏览器')
        print("当前的url",response.url)
         
        #跳到指定详情页面
        self.driver.get(response.url)
        self.driver.implicitly_wait(3)
        #print("整个页面",self.driver.page_source)
        #print(driver.title)
        #driver.save_screenshot('登录时.png')
#             get_chrome_less(driver,search_url,p)#登录并滚动到最下方
        #find_element_by_tag_name('div').text
        #user_list = response.xpath('/html//ul[@id="normal_user_container"]').extract()使用reponse时为空，因为没有用driver加载url
#         address = ','.join(response.xpath('/html//h6[@class="member_name"]/a/text()').extract())#得到多个a标签的text
#         person_info = response.xpath('/html//ul[@class="member_info_list fn-clear"]/li')#xpathy方式获取元素
        address = self.driver.find_elements_by_xpath('/html//h6[@class="member_name"]/a')#得到多个a标签的text
        str_address=''
        for addr in address:
            str_address += addr.get_attribute("text") 
        print("人员地址",str_address)
        person_info = self.driver.find_elements_by_xpath('/html//ul[@class="member_info_list fn-clear"]/li')
        #print("人员主信息",type(person_info),person_info)
        #print("person_info[2]第3条记录",person_info[2])
        #webdriver获取值
        buy_car = person_info[2].find_element_by_xpath('div[@class="fl f_gray_999"]').get_attribute("text")
        print("buy_car的属性 ",type(buy_car),buy_car)
        buy_car_info = person_info[2].find_element_by_xpath('div[@class="fl pr"]/em').text
        #buy_car = person_info[2].xpath('div/text()').extract()[0]
        #buy_car_info = person_info[2].xpath('div/em/text()').extract()
         
        #xpath方法获取item值
#         buy_car = person_info[2].xpath('div[@class="fl f_gray_999"]/text()').extract()[0]
#         buy_car_info = person_info[2].xpath('div[@class="fl f_gray_999"]//em/text()')
#         buy_car_info = person_info[2].xpath('div[@class="fl pr"]//em/text()')
        item['person_id'] = person_id
        item['buy_car'] =buy_car_info
        item['address'] = str_address
        print("buy_car_info是否购车",type(buy_car_info),buy_car_info)#未登录时这里是空的
        yield item
cmdline.execute("scrapy crawl jiayuan_slave".split())