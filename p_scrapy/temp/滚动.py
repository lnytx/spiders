# -*- coding:utf-8 -*-
'''
Created on 2018年2月28日
@author: ning.lin
'''
import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select


# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
#先登录

def get_chrome_less(driver,url):
    
    
    # chrome_options.binary_location = '/opt/google/chrome/chrome'
    
#     driver.get('https://www.baidu.com/')
    driver.get(url)
    driver.save_screenshot('1.png') 
    elem = driver.find_element_by_id("kw")
    elem.send_keys("今日热点")
    elem.send_keys(Keys.RETURN)
    time.sleep(3) 
    print('打开浏览器')
    print(driver.title)
    print("滚动")
    js="var q=document.documentElement.scrollTop=100000"  
    driver.execute_script(js)  
    driver.save_screenshot('2.png') 
    time.sleep(3)  
    driver.save_screenshot('3.png') 
    #拖动滚动条
    #找到翻页的下拉列表
    #all_pages = driver.find_element_by_id('select_box')
    #将页面定位到要查看的元素位置从而变相的实现了滚动条滚动的效果。问题解决
    #ActionChains(driver).move_to_element(all_pages).perform()  
    #用tab去啊到元素实现滚动
    #driver.find_element_by_id("select_box").send_keys(Keys.TAB)
    #鼠标移动到下拉列表下面
    #ActionChains(driver).move_to_element(all_pages).perform()
    #elem = driver.find_element_by_xpath()
    
    
    #Select(all_pages).select_by_visible_text("第3页")
    
    
    
    
    print('关闭')
    driver.quit()
    print('测试完成')
#拖动到底部   

if __name__=="__main__":
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('--disable-gpu')
    # option.add_argument("--start-maximized")
    # option.add_argument("--start-fullscreen");
    option.add_argument("--window-size=1920,1080")
    
    
    prefs = {
        'profile.default_content_setting_values': {
        'images': 2, # 不加载图片
        'javascript': 2, # 不加载JS
        }
        }
        
    option.add_experimental_option("prefs", prefs)
    
    
    driver = webdriver.Chrome(chrome_options=option)
    #url = http://search.jiayuan.com/v2/index.php?key=&sex=f&stc=&sn=default&sv=1&p=1&pt=40380&ft=off&f=select&mt=d
    url = "https://www.baidu.com"
    get_chrome_less(driver,url)
