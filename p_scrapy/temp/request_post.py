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
# url="http://search.jiayuan.com/v2/search_v2.php"

import json
import urllib.parse

import requests


url='http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%B9%BF%E5%B7%9E&kw=%E8%BF%90%E7%BB%B4&p=1&isadv=0'
a = '%E8%BF%90%E7%BB%B4'
print(urllib.parse.unquote(a))
data = {
    'sex': 'f',
    'key':'',
    'stc':'', 
    'sn': 'default',
    'sv': 2,
    'p': 9999999999,
    'f': 'select',
    'listStyle': 'bigPhoto',
    'pri_uid':'',
    'jsversion': 'v5',
}
# 1
requests.post(url, data=json.dumps(data))
requests.get(url)

# 2-json参数会自动将字典类型的对象转换为json格式
req = requests.post(url, json=data)
print(req.text)
# a = json.loads(req.text)
print(type(a),a)
