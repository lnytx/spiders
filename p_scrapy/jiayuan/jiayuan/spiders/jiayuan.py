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

from scrapy  import log
from scrapy import cmdline
import scrapy
from scrapy.http import Request
from scrapy.http.request.form import FormRequest
from scrapy_redis.spiders import RedisSpider
from selenium import webdriver

from jiayuan.settings import IMAGES_STORE,USER_NAME,PASSWD
from jiayuan.items import JiayuanItem,MainItem


class jiayuan_data(RedisSpider):
    name = "jiayuan_main"
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
    driver.find_element_by_id("login_email").send_keys(USER_NAME) #修改为自己的用户名
    driver.find_element_by_id("login_password").clear()
    driver.find_element_by_id("login_password").send_keys(PASSWD) #修改为自己的密码
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
            yield Request(url=url,cookies=self.cookies,callback=self.get_main_info)
#             yield scrapy.Request(url=search_url,callback=self.get_main_info)
#             return Request(url=url,callback=self.get_main_info)
    def get_main_info(self,response):#解析搜索业面的url
        #info = response.body.decode("utf-8")   #登录后可以查看一下登录响应信息json.loads(
#         for url in self.start_urls:
        time.sleep(1) 
        print("当前的url",response.url)
        print('重新加载url')
        self.driver.get(response.url)
        self.driver.implicitly_wait(3)
        user_list = self.driver.find_elements_by_xpath('/html//ul[@id="normal_user_container"]/li')#得到多个li标签
        if user_list==[]:
            print("下一页")
        #print("user_list",type(user_list),user_list)
        url_details = []#详情页面的url
        for user in user_list:
            url_info = user.find_elements_by_xpath('//div[@class="hy_box"]//div[@class="user_name"]/a[@class="os_stat"]')
            for url in url_info:#通过url去获取别的信息
                    main_url_main = url.get_attribute("href")
                    print("人员主页url",type(url),url.get_attribute("href"))
                    url_details.append(main_url_main)
        print("人员详情url2",len(url_details))
        if url_details!=[]:
            for url in url_details:
                yield Request(url=url,cookies=self.cookies,callback=self.get_details)
#         yield item
    def get_details(self,response):
        '''
        <class 'str'>
                            年      龄：
        26-29岁之间
                            身      高：
        169-185厘米
                            民      族：
                            汉族
                            学      历：
                            不限
                            相      册：
                            有照片
                            婚姻状况：
                            未婚
                            居  住 地：
                            湖北十堰
                            诚      信：
                            不限
                            将这种类型的文字全部转成{'学历': '不限', '婚姻状况': '未婚', '居住地': '湖北十堰', '相册': '有照片', '身高': '169-185厘米', '民族': '汉族', '诚信': '不限', '年龄': '26-29岁之间'}这种dict方便入库
        '''
        pass
        def parse(str1):
            temp_list = str1.split('\n')
            result={}
            result_str=''
#             temp_dict=[]#result_dict这是因为有些项目下面有多个标签，多个标签就需要合并起来
#             result_dict = {}#多个dict合并后的结果
            if len(temp_list)>1:#大于1说明该项下有值，否则此项未填信息
                for i in range(len(temp_list)):
                    if i%2==0:
                        result[temp_list[i].replace(" ", "").replace("：", '')] = temp_list[i+1]
                return result
            #其他则返回str
            else:
                result_str =  str1
                return result_str
             
             
        item = JiayuanItem()
        self.driver.get(response.url)
        self.driver.implicitly_wait(3)
        print('打开浏览器')
        print("当前的url",response.url)
        age_info = self.driver.find_element_by_xpath('/html//h6[@class="member_name"]').text
        person_id = response.url[response.url.rfind('/')+1:response.url.index('?')]
        print("年龄地址信息",type(age_info),age_info)
        address = self.driver.find_elements_by_xpath('/html//h6[@class="member_name"]/a')#得到多个a标签的text
        str_address=''
        str_sheng=address[0].get_attribute("text") 
        str_shi=address[1].get_attribute("text") 
        print("人员地址",str_sheng+'sssss'+str_shi)
         
        '''
        人个信息
        '''
        person_info = self.driver.find_elements_by_xpath('/html//ul[@class="member_info_list fn-clear"]')
        person_dict={}
        for i in person_info:
            person_dict = parse(i.text)
            print("个人信息",person_dict)
        '''
        处理item,对应mysql的person_info表
        '''
        item['person_id'] =  person_id
        item['province'] = str_sheng
        item['municipal'] = str_shi
        nick_name_info = self.driver.find_elements_by_xpath('/html//div[@class="member_info_r yh"]/h4')
        nick_name = nick_name_info[0].text[0:nick_name_info[0].text.index("I")]
        print("昵称", nick_name)
        item['nike_name'] = nick_name
        item['education'] = person_dict['学历']
        item['height'] = person_dict['身高']
        item['buy_car'] = person_dict['购车']
        item['salary'] = person_dict['月薪']
        item['housing'] = person_dict['住房']
        item['weight'] = person_dict['体重']
        item['constellation'] = person_dict['星座']
        item['nation'] = person_dict['民族']
        item['zodiac'] = person_dict['属相']
        item['blood_type'] = person_dict['血型']
        item['age'] = age_info[0:age_info.index('，')]
        print("年龄",age_info[0:age_info.index('，')])
        item['address'] = str_sheng+str_shi
        item['age_info'] = age_info
        item['image_dir'] = nick_name+'_'+item['age']+'_'+person_id#下载的相片归类
        item['url'] = response.url
         
        #个人短语
        item['introduce_oneself'] = self.driver.find_element_by_xpath('/html//div[@class="main_1000 mt15 fn-clear"]//div[@class="js_text"]').text
        print("个性短语",item['introduce_oneself'])
        #个性标签,有些人是没有个性标签的
        #需要点击”更多“才能全部显示出来，否则只有4个
        item['interest_label']=''
        item['personality_label']=''
        try:
            #link_a = self.driver.find_element_by_xpath('/html//div[@class="d_more DNA_xq_more DNA_xq_more_a"]/a')
            #link_a.click()
            self.driver.find_element_by_xpath('/html//div[@class="d_more DNA_xq_more DNA_xq_more_a"]/a').click()
            time.sleep(1)
            gexing_info = self.driver.find_elements_by_xpath('/html//div[@class="test4"]//div[@class="list_a fn-clear"]')
            print("aaa",type(gexing_info),gexing_info)
            gexing_tag=''
            for i in gexing_info:
                gexing_tag += i.text
    #             a = item.find_element_by_xpath('div[@class="pag_list_grey_c"]').text
            item['personality_label'] = "".join(gexing_tag)
        except Exception as e:
            item['personality_label'] = '还没有填写个性元素'
        print("个性",item['personality_label'])
        #她的兴趣爱好有可能也是找不到的   
        try:
            #link_a = self.driver.find_element_by_xpath('/html//div[@class="d_more DNA_xq_more DNA_xq_more_a"]/a')
            #link_a.click()
            self.driver.find_element_by_xpath('/html//div[@class="d_more DNA_xq_more"]/a').click()
#             self.driver.find_element_by_xpath('/html/body/div[6]/div[1]/div[3]/div/div[1]/div[2]/a').click
            self.driver.implicitly_wait(1)
            aihao_info = self.driver.find_elements_by_xpath('/html/body/div[6]/div[1]/div[3]/div/div[1]/div[1]/ul')
            print("bbb",type(aihao_info),aihao_info)
            aihao_tag=''
            for i in aihao_info:
                aihao_tag += i.text 
    #             a = item.find_element_by_xpath('div[@class="pag_list_grey_c"]').text
            item['interest_label'] = "".join(aihao_tag)
        except Exception as e:
            item['interest_label'] = '还没有填写兴趣爱好'
        print("她的兴趣爱好",item['interest_label'])
        find_mate = self.driver.find_elements_by_xpath('/html//div[@class="bg_white mt15"]')
        '''
        择偶要求
        '''
        mate = find_mate[1].find_elements_by_xpath('div[@class="js_box"]/ul[@class="js_list fn-clear"]')
        mate_dict={}
        for i in mate:
            mate_dict = parse(i.text)
        item['person_id_mate'] =  person_id
        item['age_mate'] = mate_dict['年龄']
        item['height_mate'] = mate_dict['身高']
        item['nation_mate'] = mate_dict['民族']
        item['education_mate'] = mate_dict['学历']
        item['image_mate'] = mate_dict['相册']
        item['marital_status'] = mate_dict['婚姻状况']
        item['address_mate'] = mate_dict['居住地']
        item['sincerity_mate'] = mate_dict['诚信']#诚信
        print("择偶要求",mate_dict)
        '''
            生活方式
        '''
        life = find_mate[2].find_elements_by_xpath('div[@class="js_box"]/ul[@class="js_list fn-clear"]')
        life_style={}
        for i in life:
            temp = parse(i.text)
            if isinstance(temp,dict):
                    life_style.update(parse(i.text))#update就合并两个dict
            else:
                life_style['吸烟'] = '未填写生活方式'
                life_style['饮酒'] = '未填写生活方式'
                life_style['锻炼习惯'] = '未填写生活方式'
                life_style['饮食习惯'] = '未填写生活方式'
                life_style['逛街购物'] = '未填写生活方式'
                life_style['宗教信仰'] = '未填写生活方式'
                life_style['作息时间'] = '未填写生活方式'
                life_style['交际圈子'] = '未填写生活方式'
                life_style['最大消费'] = '未填写生活方式'
        try:
            housework = []
            pet = []
            jiawu1 = find_mate[2].find_elements_by_xpath('div[@class="js_box"]//div[@class="pt25 fn-clear"]//dd[@class="cur"]')
            for i in jiawu1:
                housework.append(i.text)#0为家务水平，1为宠物喜欢程度
                print("家务1 ",i.text)
            jiawu2 = find_mate[2].find_elements_by_xpath('div[@class="js_box"]//div[@class="fl pr"]/em')
            for i in jiawu2:
                pet.append(i.text)#0为家务分配，1为关于宠物
                print("家务2 ",i.text)
        except Exception as e:
            housework.append('家务水平程度未填写')
            housework.append('宠物喜欢程度未填写')
            pet.append('家务分配未填写')
            pet.append ('关于宠物未填写')
        item['person_id_life'] =  person_id
        item['smoke'] = life_style['吸烟']
        item['drink_wine'] = life_style['饮酒']
        item['exercise_habits'] = life_style['锻炼习惯']
        item['eating_habits'] = life_style['饮食习惯']
        item['shopping'] = life_style['逛街购物']
        item['religious_belief'] = life_style['宗教信仰']
        item['time_table'] = life_style['作息时间']
        item['circle_of_communication'] = life_style['交际圈子']
        item['maximum_consumption'] = life_style['最大消费']
        item['housework'] = housework[0]
        item['household_assignment'] = pet[0]
        item['pet'] = housework[1]
        item['about_pets'] = pet[1]
        print("生活方式",life_style)
        print("家务",housework[0],pet[0])
        print("宠物",housework[1],pet[1])
        '''
        经济实力
        '''
        economic_dict={}
        economic = find_mate[3].find_elements_by_xpath('div[@class="js_box"]/ul[@class="js_list fn-clear"]')
        for i in economic:
            economic_dict = parse(i.text)
        item['person_id_economic'] =  person_id
        item['salary_economic'] =  economic_dict['月薪']
        item['buy_house_economic'] =  economic_dict['购房']
        item['buy_car_economic'] =  economic_dict['购车']
        item['economic_concept'] =  economic_dict['经济观念']
        item['investment_financing'] =  economic_dict['投资理财']
        item['foreign_debt'] =  economic_dict['外债贷款']
        print("经济实力",economic_dict)
        '''
        工作学习
        '''
        work = find_mate[4].find_elements_by_xpath('div[@class="js_box"]/ul[@class="js_list fn-clear"]')
        work_study = {}#
        for i in work:
            if i.text:
                temp = parse(i.text)
                if isinstance(temp,dict):
                    work_study.update(parse(i.text))#update就合并两个dict
                else:
                    work_study['职业职位'] = '未填写工作学习方式'
                    work_study['公司行业'] = '未填写工作学习方式'
                    work_study['公司类型'] = '未填写工作学习方式'
                    work_study['福利待遇'] = '未填写工作学习方式'
                    work_study['工作状态'] = '未填写工作学习方式'
                    work_study['调动工作可能性'] = '未填写工作学习方式'
                    work_study['事业与家庭'] = '未填写工作学习方式'
                    work_study['海外工作可能性'] = '未填写工作学习方式'
                    work_study['毕业院校'] = '未填写工作学习方式'
                    work_study['专业类型'] = '未填写工作学习方式'
                    work_study['语言能力'] = '未填写工作学习方式'
        item['person_id_study'] =  person_id
        item['position'] =  work_study['职业职位']
        item['company'] =  work_study['公司行业']
        item['company_type'] =  work_study['公司类型']
        item['welfare'] =  work_study['福利待遇']
        item['working'] =  work_study['工作状态']
        item['transfer_work'] =  work_study['调动工作可能性']
        item['work_family'] =  work_study['事业与家庭']
        item['overseas_job'] =  work_study['海外工作可能性']
        item['university'] =  work_study['毕业院校']
        item['major'] =  work_study['专业类型']
        item['language'] =  work_study['语言能力']
        print("工作学习",work_study)
        '''
        婚姻观念
        '''
        marriage = find_mate[5].find_elements_by_xpath('div[@class="js_box"]/ul[@class="js_list fn-clear"]')
        marriage_family={}
        for i in marriage:
            if i.text:
                temp = parse(i.text)
                if isinstance(temp,dict):
                    marriage_family.update(parse(i.text))#update就合并两个dict
                else:
                    marriage_family['籍贯'] = '未填写婚姻观念'
                    marriage_family['户口'] = '未填写婚姻观念'
                    marriage_family['国籍'] = '未填写婚姻观念'
                    marriage_family['个性待征'] = '未填写婚姻观念'
                    marriage_family['幽默感'] = '未填写婚姻观念'
                    marriage_family['脾气'] = '未填写婚姻观念'
                    marriage_family['对待感情'] = '未填写婚姻观念'
                    marriage_family['是否要小孩'] = '未填写婚姻观念'
                    marriage_family['何时结婚'] = '未填写婚姻观念'
                    marriage_family['是否能接受异地恋'] = '未填写婚姻观念'
                    marriage_family['理想婚姻'] = '未填写婚姻观念'
                    marriage_family['愿与对方父母同住'] = '未填写婚姻观念'
                    marriage_family['家中排行'] = '未填写婚姻观念'
                    marriage_family['父母情况'] = '未填写婚姻观念'
                    marriage_family['兄弟姐妹'] = '未填写婚姻观念'
                    marriage_family['父母经济情况'] = '未填写婚姻观念'
                    marriage_family['父母医保情况'] = '未填写婚姻观念'
                    marriage_family['父母的工作'] = '未填写婚姻观念'
        item['person_id_marriage'] =  person_id
        item['address_marriage'] =  marriage_family['籍贯']
        item['registered_residence'] =  marriage_family['户口']
        item['nationality'] =  marriage_family['国籍']
        item['personality'] =  marriage_family['个性待征']
        item['humor'] =  marriage_family['幽默感']
        item['temper'] =  marriage_family['脾气']
        item['feelings'] =  marriage_family['对待感情']
        item['want_child'] =  marriage_family['是否要小孩']
        item['when_mary'] =  marriage_family['何时结婚']
        item['strange_love'] =  marriage_family['是否能接受异地恋']
        item['ideal_marriage'] =  marriage_family['理想婚姻']
        item['live_parents'] =  marriage_family['愿与对方父母同住']
        item['rankings_home'] =  marriage_family['家中排行']
        item['parents_situation'] =  marriage_family['父母情况']
        item['brothers'] =  marriage_family['兄弟姐妹']
        item['parents_economic'] =  marriage_family['父母经济情况']
        item['parents_medical'] =  marriage_family['父母医保情况']
        item['parents_working'] =  marriage_family['父母的工作']
        print("婚姻观念",marriage_family)
        '''
        相片列表
        '''
        #获取图片
        print("相片url",response.url)
        list_images = self.driver.find_elements_by_xpath('/html//div[@id="bigImg"]//a')
        print("相片列表",type(list_images),list_images)
        images= []
        for i in list_images:
            image = i.find_element_by_xpath('img').get_attribute("src")
            images.append(image)
            print("相片地址",image)
         
        item['img_urls'] = images#保存相片地址，在person_info表中的text
        print("执行到了最后执行到了最后执行到了最后执行到了最后执行到了最后执行到了最后执行到了最后")
        yield item
cmdline.execute("scrapy crawl jiayuan_main".split())