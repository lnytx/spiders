# -*- coding:utf-8 -*-
'''
Created on 2018年2月28日
@author: ning.lin
'''
import json

from scrapy import cmdline
import scrapy
from scrapy.http.request.form import FormRequest
from selenium import webdriver



class SpiderCsdnSpider(scrapy.Spider):
    name = "jiayuan1"
    allowed_domains = ["jiayuan.com"]
    start_urls = [
        "http://login.jiayuan.com/",
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
        return  scrapy.FormRequest.from_response(response,
                                          url=post_url,   #真实post地址
                                          meta={'cookiejar':response.meta['cookiejar']},
                                          formdata=post_data,
                                          dont_filter=True,
                                          callback=self.next
                                          )
    
    def next(self,response):
        print("response的 值",response.url)
        body = response.body
        a = response.body.decode("utf-8")   #登录后可以查看一下登录响应信息
        print("登录后的body",a)
        my_url = "http://www.jiayuan.com/usercp/?from=login"
        #yield scrapy.FormRequest(url=my_url, callback=self.parse)
        #查取所有女性数据，去掉地区，年龄，身高等手动点击处理掉
        search_url = "http://search.jiayuan.com/v2/index.php?key=&sex=f&stc=&sn=default&sv=1&p=1&pt=56114&ft=off&f=select&mt=d"
        yield scrapy.Request(url=search_url, callback=self.parse)
        #yield scrapy.Request(url=my_url,callback=self.pase)
        """登录后请求需要登录才能查看的页面，如个人中心，携带授权后的Cookie请求"""
        #yield Request('http://edu.iqianyue.com/index_user_index.html',meta={'cookiejar':True},callback=self.next2)
    
    def parse(self,response):
        print("获取个人主页jiayuan1")
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
        for item in user_list:
            print("人员列表",type(item),item)
            #print("人员列表",type(item),item.xpath('//div[@class="search_userHead"]').extract())
        #infolist = json.loads(string)['userInfo']
        #print("信息汇总",type(infolist),infolist)
        #for info_one in infolist:
            #print("info_one人员信息",info_one)
        
        
        
#         title = response.xpath('/html/head/title/text()').extract()[0]
#         print("多么多么神烦警探 ",title )
#         if title=='佳缘登录页_世纪佳缘交友网':
#             print("登录成功")
#         sites = response.xpath('//div//a')
#         for site in sites:
#             print("//a标签",site)
#             link = site.xpath('@href').extract()
#             item['link'] = link
#             desc = site.xpath('text()').extract()
#             item['desc'] = desc
#             title = site.xpath('a/text()')
#             #返回信息
#             yield item
#         print("捉取",response.body)
#         print("头部信息",response.request.headers['User-Agent'])
#         yield item



'''
可在spiders目录下建一个run.py可代替在终端输入命令。
'''
from scrapy import cmdline

cmdline.execute("scrapy crawl jiayuan1".split())