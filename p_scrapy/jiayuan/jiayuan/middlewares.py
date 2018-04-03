# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html



class Jiayuan2SpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class Jiayuan2DownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)



'''
自定义的使用selenium中间件
        '''
#这里将webdriver定义在spider文件的好处是，不需要每一次请求url都打开和关闭浏览器
        #head less模拟登录
'''
定义全局的driver防止一直被实例化
'''
import re

import redis
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver

from jiayuan.settings import USER_NAME, PASSWD
global driver
global r
login_url = 'http://login.jiayuan.com/'#登录时的url
option = webdriver.ChromeOptions()
prefs={"profile.managed_default_content_settings.images":2}#禁止加载图片
option.add_experimental_option("prefs",prefs)
option.add_argument('--headless')
option.add_argument("--window-size=1920,1080")
# option.add_argument("--proxy-server=http://222.73.68.144:8090")
pool=redis.ConnectionPool(host='127.0.0.1',port=6379,db=0,decode_responses=True)  #427条记录
r = redis.StrictRedis(connection_pool=pool)  
redis_pipe = r.pipeline()
print("登录中",USER_NAME)
try:
    driver = webdriver.Chrome(chrome_options=option)
    driver.get(login_url)#登录页面
#     print(driver.page_source)
    import time
    time.sleep(3)
    driver.find_element_by_id("login_btn").click()
    driver.find_element_by_id("login_email").clear()
    driver.find_element_by_id("login_email").send_keys(USER_NAME) #修改为自己的用户名
    driver.find_element_by_id("login_password").clear()
    driver.find_element_by_id("login_password").send_keys(PASSWD) #修改为自己的密码
    #登录url
    #url="http://login.jiayuan.com/"
    driver.find_element_by_id("login_btn").click()#点击登录按钮
    #登录url
    #url="http://login.jiayuan.com/"
    driver.find_element_by_id("login_btn").click()#点击登录按钮
    driver.implicitly_wait(3)
    title = driver.title;
    print("页面的title",type(title),title)
    if title =='佳缘登录页_世纪佳缘交友网':
        print("已成功登录执行了页面")
except Exception as e:
    driver.close()
    print("spider出现了异常,关闭",str(e))
        
#         print("已登录",driver.page_source)
class SeleniumMiddleware(object):
    def process_request(self, request, spider):
        
#         if request.meta.has_key('PhantomJS'): #当请求经过下载器中间件时,检查请求中是否有这个meta,决定这个请求要不要使用中间件。
#             driver = webdriver.PhantomJS() 
#             driver.get(request.url) 
#             content = driver.page_source.encode('utf-8') 
#             driver.quit() 
#             return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)
        global driver
        global r
        #根据url判断是详情页面还是人员列表页
        main = 'http://search.jiayuan.com/v2/index.php?key=&sex=f&stc=&sn=default&sv=1&p='
        deatils = 'http://www.jiayuan.com/\d+\?fxly=.*'
        if main in request.url:
            print("当前中间件URL为人员列表页，要从中提取人员主页返回spider",request.url)
            driver.get(request.url)
#             html_source = driver.page_source
            #获取详情url
            user_list = driver.find_elements_by_xpath('/html//ul[@id="normal_user_container"]/li')#得到多个li标签
            print("user_list",user_list)
            if user_list==[]:
                print("user_list为空了下一页")
            #print("user_list",type(user_list),user_list)
            url_details = []#详情页面的url
            for user in user_list:
                url_info = user.find_elements_by_xpath('//div[@class="hy_box"]//div[@class="user_name"]/a[@class="os_stat"]')
                for url in url_info:#通过url去获取别的信息
                    main_url_main = url.get_attribute("href")
                    print("人员主页url",type(url),url.get_attribute("href"))
                    print(" 写入redis")
                    redis_pipe.rpush ('jiyuan_aaa:person_url',main_url_main)
                    url_details.append(main_url_main)
                redis_pipe.execute()
                r.save()

            ret_url_details = bytes(','.join(url_details), encoding = "utf8")
            #返回当前所有的人员详情的URL，需要先转换str再使用bytes才能放入body中
            return HtmlResponse(url=driver.current_url,body=ret_url_details,
                    encoding="utf-8", request=request)
        elif re.findall(deatils,request.url):
            print("传入的是人员详情url，返回人员页面",request.url)
            driver.get(request.url)
            html_source = driver.page_source
            return HtmlResponse(url=driver.current_url,body=html_source,
                    encoding="utf-8", request=request)
    def closed(self,spider):
        print("spider closed")
        driver.close()