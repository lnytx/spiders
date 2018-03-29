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
from scrapy  import log
from scrapy import cmdline
import scrapy
from scrapy.http.request.form import FormRequest
from selenium import webdriver
from jiayuan.items import JiayuanItem


class jiayuan_data(scrapy.Spider):
    name = "jiayuan"
    allowed_domains = ["jiayuan.com"]
    start_urls = [
        "http://usercp.jiayuan.com/?from=login/",
        #"https://passport.jiayuan.com/dologin.php?pre_url=http://www.jiayuan.com/usercp",#登录页面post数据
    ]
    '''
        下载器中间件在下载器和Scrapy引擎之间，每一个request和response都会通过中间件进行处理。
        在中间件中，对request进行处理的函数是process_request(request, spider)
    '''
    def start_requests(self):#
        login_url = 'http://login.jiayuan.com/'  # 登录页面
        return [scrapy.Request(url=login_url,meta={'cookiejar':1},callback=self.login)]
    
    def login(self, response):
        print("login 值",response.url)
        _s_x_id = response.xpath("//input[@name='_s_x_id']/@value").extract_first()
        print("_s_x_id的值",_s_x_id)
        if _s_x_id is None:
            return ''
        post_url = 'https://passport.jiayuan.com/dologin.php?pre_url=http://www.jiayuan.com/usercp'    # 这里是输入手机号
        post_data = {
            "name":"lnytx@163.com",
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
        #找成return就有问题了
        return  [scrapy.FormRequest.from_response(response, url=post_url, meta={'cookiejar':response.meta['cookiejar']},formdata=post_data,dont_filter=True,callback=self.after_login)]
    
    
    def after_login(self,response):
        print("after_login的 值",response.url)
#         print("获取个人主页jiayuan",response)
#         print("页面%s"%(response.url),response.text)
        current_url = response.url #爬取时请求的url
        body = response.body  #返回的html
        #unicode_body = response.body_as_unicode()#返回的html unicode编码
        string = response.text
        print("查询的主页",string)
        #user_list = response.xpath('/html//ul[@id="normal_user_container"]').extract()
        #搜索结果在http://search.jiayuan.com/v2/search_v2.php
        user_list = response.xpath('//div[contains(@class,"search_userHead")]')
        print("人员列表user_list",type(user_list),user_list)
        #a[last()]/@href'
#         for item in user_list:
#             print("人员列表",type(item),item)
        search_url = "http://search.jiayuan.com/v2/search_v2.php"#查询的url,可以取到json
        return scrapy.Request(url=search_url,meta={'cookiejar':1},callback=self.next)   
    
    
    def next(self,response):
        print("next的 值",response.url)
        body = response.body
        info = json.loads(response.body.decode("utf-8"))   #登录后可以查看一下登录响应信息
        print("登录后的body",info)#直接使用这里面的href也可以登录
        print("总的页数",info['pageTotal'])
        print("总的人数",info['count'])
        print("是否登录",info['isLogin'])
        print("当前userinfo个数",len(info['userInfo']))
        
        my_url = "http://www.jiayuan.com/usercp/?from=login"
        #yield scrapy.FormRequest(url=my_url, callback=self.parse)
        #查取所有女性数据，去掉地区，年龄，身高等手动点击处理掉
        #佳缘网获取搜索页面数据api,直接可以获取到json
        #手动构建url循环查询
#         search_url = "http://search.jiayuan.com/v2/index.php?key=&sex=f&stc=&sn=default&sv=1&p=%s&pt=%s&ft=off&f=select&mt=d"
#         search_data = {
#             "sex":"f",
#             "key":"",
#             "stc":"",#条件是只选取女性
#             "sn":"default",
#             "sv":"1",
#             "p":"1",
#             "f":"select",
#             "listStyle":"bigPhoto",
#             "pri_uid":"68209968", #自己账户的realUid
#             "jsversion":"v5"
#         }
#         request = FormRequest(search_url,callback=self.parse,formdata=search_data)
#         yield FormRequest(search_url,callback=self.parse,formdata=search_data)
        #search_url = "http://search.jiayuan.com/v2/index.php?key=&sex=f&stc=&sn=default&sv=1&p=1&pt=56114&ft=off&f=select&mt=d"
        print("执行搜索")
        '''
                                        启用headless chrome 异步加载脚本
        '''
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        # option.add_argument("--start-maximized")
        # option.add_argument("--start-fullscreen");
        option.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(chrome_options=option)
        page_count=0
        #当前页
        for p in range(1,int(info['pageTotal']+1)):
            page_count+=1
            search_url = "http://search.jiayuan.com/v2/index.php?key=&sex=f&stc=&sn=default&sv=1&p=%s&pt=%s&ft=off&f=select&mt=d" %(p,info['pageTotal'])
            #用户webdrive的方法获取动态加载的数据
            driver.get(search_url)
            time.sleep(3) 
            print('打开浏览器')
            print("当前的url",search_url)
            print(driver.title)
            #driver.save_screenshot('登录时.png')
#             get_chrome_less(driver,search_url,p)#登录并滚动到最下方
            print("p的页数",p)
            print("page_count的页数",page_count)
            #find_element_by_tag_name('div').text
            #user_list = response.xpath('/html//ul[@id="normal_user_container"]').extract()使用reponse时为空，因为没有用driver加载url
            user_list = driver.find_elements_by_xpath('/html//ul[@id="normal_user_container"]/li')#得到多个li标签
            #print("user_list",type(user_list),user_list)
            item = JiayuanItem()
            person_count=0
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
                        print("人员主页url",type(url),url.get_attribute("href"))
                        print("昵称",url.get_attribute("text"))
                        ss=url.find_element_by_xpath('../../p[@class="user_info"]')
                        print("年龄_城市",ss.text,type(ss))
                        hh=url.find_element_by_xpath('../../p[@class="zhufang"]').find_element_by_tag_name('span')
                        item['user_info'] = ss.text
                        item['nick_name'] = url.get_attribute("text")
                        item['main_url'] = url.get_attribute("href")
                        print("身高",hh.text,type(hh),hh)
                        item['heigth'] = hh.text
                        yield item
                    except Exception as error:
                        log(error)
#                     if p==2:
#                     break   
            #driver.find_element_by_xpath("//a[text()='第2页'+]").click()
            #p +=1;
            #yield  scrapy.Request(url=search_url,meta={'cur_page':p},callback=self.parse)
        #yield scrapy.Request(url=my_url,callback=self.pase)
        #"""登录后请求需要登录才能查看的页面，如个人中心，携带授权后的Cookie请求"""
        #yield Request('http://edu.iqianyue.com/index_user_index.html',meta={'cookiejar':True},callback=self.next2)
        
    def parse(self,response):
        print("parse的 值",response.url)
        #print("获取个人主页jiayuan",response.body.decode("utf-8"))
        print("上次的meta参数",response.meta['cur_page'])
        title = response.xpath('/html/head/title/text()').extract()
        print("页面头部信息",title)
#         print("页面%s"%(response.url),response.text)
        current_url = response.url #爬取时请求的url
        body = response.body.decode("utf-8")  #返回的html
        print("body",body)
        #unicode_body = response.body_as_unicode()#返回的html unicode编码
        string = response.text
        #用户webdrive的方法获取动态加载的数据
        user_list = response.xpath('/html//ul[@id="normal_user_container"]').extract()
        print("user_list",user_list)
        for item in user_list:
            print("人员列表",type(item),item)
        
cmdline.execute("scrapy crawl jiayuan".split())