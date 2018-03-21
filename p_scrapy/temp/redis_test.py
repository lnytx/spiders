# -*- coding:utf-8 -*-
'''
Created on 2018年2月28日
@author: ning.lin
'''
import redis


if __name__=="__main__":
#     option = webdriver.ChromeOptions()
#     option.add_argument('--headless')
#     option.add_argument("--window-size=1920,1080")
#     driver = webdriver.Chrome(chrome_options=option)
#     url = "http://search.jiayuan.com/v2/index.php?key=&sex=f&stc=&sn=default&sv=1&p=1&pt=4467&ft=off&f=select&mt=d"
#     login(driver)
#     get_chrome_less(driver,url)
    r = redis.Redis(host="127.0.0.1",port=6379,db=0)
    r.set('foo','test')
    pass