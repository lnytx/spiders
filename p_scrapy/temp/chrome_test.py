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
def login(driver):
    url = 'http://login.jiayuan.com/'
    driver.get(url)
    time.sleep(20) 
    driver.find_element_by_id("login_btn").click()
    driver.find_element_by_id("login_email").clear()
    driver.find_element_by_id("login_email").send_keys("这是我的用户名") #修改为自己的用户名
    driver.find_element_by_id("login_password").clear()
    driver.find_element_by_id("login_password").send_keys("*******************") #修改为自己的密码
    #登录url
    #url="http://login.jiayuan.com/"
    driver.find_element_by_id("login_btn").click()#点击登录按钮
    cookies = driver.get_cookies()
    time.sleep(10)
    driver.save_screenshot('login1.png')
    cookies = driver.get_cookies()
    print ("cookies",cookies)
    return cookies
def get_chrome_less(driver,url,cur_page):
    
    
    # chrome_options.binary_location = '/opt/google/chrome/chrome'
    
#     driver.get('https://www.baidu.com/')
    driver.get(url)
    time.sleep(5) 
    print('打开浏览器')
    print(driver.title)
    #driver.save_screenshot('登录时.png')
    #滚动到底部
    scroll(driver)
    #driver.save_screenshot('滚动条下拉.png') 
#     all_pages = driver.find_element_by_id("select_box")
#     print("元素是否显示",all_pages.is_displayed())
#     #将页面定位到要查看的元素位置从而变相的实现了滚动条滚动的效果。问题解决
#     ActionChains(driver).move_to_element(all_pages).perform()  
    #driver.save_screenshot('定位鼠标上.png') 
    #用tab去啊到元素实现滚动
    #driver.find_element_by_id("select_box").send_keys(Keys.TAB)
    #鼠标移动到下拉列表下面
    #ActionChains(driver).move_to_element(all_pages).perform()
    #elem = driver.find_element_by_xpath()
    
    
    #driver.find_element_by_link_text("第3页").click()
    #driver.find_element_by_xpath("//a[text()='第3页']").click()
    #scroll()
    #driver.save_screenshot('点击第三页图标.png') 
    
    '''
            获取节点及其元素
    '''
    #ss = driver.find_element_by_xpath("//div[contains(@class,'big')]")
#     user_info = driver.find_element_by_xpath('//ul[@id="normal_user_container"]/li')
#     #/div/div[@class="user_name"]/a.get_attribute("href")
#     print("这是人员信息的链接",type(user_info),user_info)
#     for i in user_info:
#         print("节点",i)
    
    
    
    
    
    print('关闭')
    driver.delete_all_cookies()#删除cookies
    driver.quit()
    print('测试完成')
    
#拖动滚动条到底部   
def  scroll(driver):
    time.sleep(2) 
    js="var q=document.documentElement.scrollTop=100000"  
    driver.execute_script(js)  
    time.sleep(2)
     
if __name__=="__main__":
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(chrome_options=option)
    url='https://171466.com/Lottery/index/bet/27'
    print(driver.page_source)
#     url = "http://search.jiayuan.com/v2/index.php?key=&sex=f&stc=&sn=default&sv=1&p=1&pt=4467&ft=off&f=select&mt=d"
#     login(driver)
#     get_chrome_less(driver,url)
    s = '莹♪♪'
    f2='c.txt'
    with open(f2,'w',encoding= 'utf-8') as mon:  
        mon.write(s)
    print("s",s)
