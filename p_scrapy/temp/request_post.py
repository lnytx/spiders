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


import requests
import json
url="http://search.jiayuan.com/v2/search_v2.php"
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
# 2-json参数会自动将字典类型的对象转换为json格式
req = requests.post(url, json=data)
a = json.loads(req.text)
print(type(a),a)
