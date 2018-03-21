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

from jiayuan_details.items import JiayuanDetails


class jiayuan_redis(scrapy.Spider):
    name = "spider_redis"
    allowed_domains = ["jiayuan.com"]
    start_urls = [
        "http://search.jiayuan.com/v2/search_v2.php",#直接搜索结果，获取个人主页的url(先不登录)
        #"https://passport.jiayuan.com/dologin.php?pre_url=http://www.jiayuan.com/usercp",#登录页面post数据
    ]
    '''
        下载器中间件在下载器和Scrapy引擎之间，每一个request和response都会通过中间件进行处理。
        在中间件中，对request进行处理的函数是process_request(request, spider)
    '''
    def start_requests(self):#
        return [scrapy.Request(url=self.start_urls[0],meta={'cookiejar':1},callback=self.get_count_info)]
    def get_count_info(self,response):
        print("next的 值",response.url)
        body = response.body
        info = json.loads(response.body.decode("utf-8"))   #登录后可以查看一下登录响应信息
        print("登录后的body",info)#直接使用这里面的href也可以登录
        print("总的页数",info['pageTotal'])
        print("总的人数",info['count'])
        print("是否登录",info['isLogin'])
        print("当前userinfo个数",len(info['userInfo']))
        print("获取个人主页jiayuan",response)
        
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        option.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(chrome_options=option)
        page_count=0
        for p in xrange(1,int(info['pageTotal']+1)):
            page_count+=1
            search_url = "http://search.jiayuan.com/v2/index.php?key=&sex=f&stc=&sn=default&sv=1&p=%s&pt=%s&ft=off&f=select&mt=d" %(p,info['pageTotal'])
            #用户webdrive的方法获取动态加载的数据
            driver.get(search_url)
            time.sleep(3) 
            print('打开浏览器')
            print("当前的url",search_url)
            #print(driver.title)
            #driver.save_screenshot('登录时.png')
#             get_chrome_less(driver,search_url,p)#登录并滚动到最下方
            print("p的页数",p)
            print("page_count的页数",page_count)
            #find_element_by_tag_name('div').text
            #user_list = response.xpath('/html//ul[@id="normal_user_container"]').extract()使用reponse时为空，因为没有用driver加载url
            user_list = driver.find_elements_by_xpath('/html//ul[@id="normal_user_container"]/li')#得到多个li标签
            #print("user_list",type(user_list),user_list)
            item = JiayuanDetails()
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
                        print("身高",item['heigth'])
                        
                        yield item
                    except Exception as error:
                        log(error)     
        
cmdline.execute("scrapy crawl spider_redis".split())