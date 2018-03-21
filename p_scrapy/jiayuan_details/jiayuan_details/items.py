# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JiayuanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    person_id = scrapy.Field()#人员唯一ID
    user_info = scrapy.Field()#搜索页面中的年龄与所属城市
    main_url = scrapy.Field()#搜索页面中人员入口url
    nick_name = scrapy.Field()#搜索页面中人员昵称
    heigth = scrapy.Field()#搜索页面中身高
    
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