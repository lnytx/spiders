# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MainItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    person_id_main = scrapy.Field()#人员唯一ID
    user_info_main = scrapy.Field()#搜索页面中的年龄与所属城市
    main_url_main = scrapy.Field()#搜索页面中人员入口url
    nick_name_main = scrapy.Field()#搜索页面中人员昵称
    heigth_main = scrapy.Field()#搜索页面中身高

class JiayuanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    person_id_main = scrapy.Field()#人员唯一ID
    user_info_main = scrapy.Field()#搜索页面中的年龄与所属城市
    main_url_main = scrapy.Field()#搜索页面中人员入口url
    nick_name_main = scrapy.Field()#搜索页面中人员昵称
    heigth_main = scrapy.Field()#搜索页面中身高
    
    
        #person_info表
    nike_name = scrapy.Field()#昵称
    person_id = scrapy.Field()
    province = scrapy.Field()#省
    municipal = scrapy.Field()#市
    image_dir = scrapy.Field()
    age = scrapy.Field()
    sex = scrapy.Field()
    age_info = scrapy.Field()#年龄地址信息
    education = scrapy.Field()#学历
    height = scrapy.Field()
    buy_car = scrapy.Field()
    address = scrapy.Field()
    salary = scrapy.Field()
    housing = scrapy.Field()#住房
    constellation = scrapy.Field()#星座
    nation = scrapy.Field()#民族
    weight = scrapy.Field()
    zodiac = scrapy.Field()#生肖
    blood_type = scrapy.Field()#血型
    introduce_oneself = scrapy.Field()#自我介绍
    interest_label = scrapy.Field()#兴趣爱好
    personality_label = scrapy.Field()#个人标签
    img_urls = scrapy.Field()#相片url保存地址
    url = scrapy.Field()#人个主页url
    image_dir = scrapy.Field()#下载的相片目录
    
    #mate_selection择偶标准表
    person_id_mate = scrapy.Field()
    age_mate = scrapy.Field()
    height_mate = scrapy.Field()
    nation_mate = scrapy.Field()
    education_mate = scrapy.Field()
    image_mate = scrapy.Field()#是否有相片
    marital_status = scrapy.Field()#婚姻状况
    address_mate = scrapy.Field()
    sincerity_mate = scrapy.Field()#诚信
    #life_style生活方式表
    person_id_life = scrapy.Field()
    smoke = scrapy.Field()
    drink_wine = scrapy.Field()
    exercise_habits = scrapy.Field()#锻炼习惯
    eating_habits = scrapy.Field()#饮食习惯
    shopping = scrapy.Field()#逛街购物
    religious_belief = scrapy.Field()#宗教信仰
    time_table = scrapy.Field()#作息时间
    circle_of_communication = scrapy.Field()#交际圈子
    maximum_consumption = scrapy.Field()#最大消费
    housework = scrapy.Field()#家务
    household_assignment = scrapy.Field()#家务分配
    pet = scrapy.Field()
    about_pets = scrapy.Field()#关于宠物
    
    #economic_strength经济实力表
    person_id_economic = scrapy.Field()
    salary_economic = scrapy.Field()
    buy_house_economic = scrapy.Field()
    buy_car_economic = scrapy.Field()
    economic_concept = scrapy.Field()#经济观念
    investment_financing = scrapy.Field()#投资理财
    foreign_debt = scrapy.Field()#外债贷款
    
    #work_study工作与学习表
    person_id_study = scrapy.Field()
    position = scrapy.Field()#职业职位
    company = scrapy.Field()#公司行业
    company_type = scrapy.Field()
    welfare = scrapy.Field()#福利待遇
    working = scrapy.Field()#工作状况
    transfer_work = scrapy.Field()#调动工作可能性
    work_family = scrapy.Field()#事业与家庭
    overseas_job = scrapy.Field()#海外工作可能性
    university = scrapy.Field()#毕业院校
    major = scrapy.Field()#专业类型
    language = scrapy.Field()#语言能力
    
    #marriage_concep婚姻观念表
    person_id_marriage = scrapy.Field()
    address_marriage  = scrapy.Field()#籍      贯
    registered_residence = scrapy.Field()#户口
    nationality = scrapy.Field()#国      籍
    personality = scrapy.Field()#个性特征
    humor = scrapy.Field()#幽  默 感
    temper = scrapy.Field()#脾      气
    feelings = scrapy.Field()#对待感情
    want_child = scrapy.Field()#是否要小孩
    when_mary = scrapy.Field()#何时结婚
    strange_love = scrapy.Field()#是否能接受异地恋
    ideal_marriage = scrapy.Field()#理想婚姻
    live_parents = scrapy.Field()#愿与对方父母同住
    rankings_home = scrapy.Field()#家中排行
    parents_situation = scrapy.Field()#父母情况
    brothers = scrapy.Field()#兄弟姐妹
    parents_economic = scrapy.Field()#父母经济情况
    parents_medical = scrapy.Field()#父母医保情况
    parents_working = scrapy.Field()#父母的工作
    
    
    
    
class PersonInfo((scrapy.Item)):
    #person_info人员信息表
    person_id = scrapy.Field()
    buy_car = scrapy.Field()
    address = scrapy.Field()
    
class OtherItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    '''
            可以定义另外一个item
    '''
    user_info = scrapy.Field()#搜索页面中的年龄与所属城市
    main_url = scrapy.Field()#搜索页面中人员入口url
    nick_name = scrapy.Field()#搜索页面中人员昵称
    heigth = scrapy.Field()#搜索页面中身高