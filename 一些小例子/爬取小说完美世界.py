'''
Created on 2017年5月9日

@author: ning.lin
'''

import urllib
import re
import os
import codecs
import requests
def getBookMemu(url_path):
    menu_patten = '<dd>.*?</dd>'
    url_chapter = '<dd><a href="(.*)">(.*)</a></dd>'
    thePage = requests.get(url_path)
    page = thePage.text
    menu_list = re.findall(menu_patten, page)
    menu = dict() # map<url, chapter>
    for chapter in menu_list:
        g = re.match(url_chapter, chapter)
        if g:
            menu[url_path+g.group(1)] = g.group(2)
    return menu
    pass;
 
def getContent(url_path):
    cc = str()
    thePage = requests.get(url_path)
    page = str(thePage.read()).decode('gbk')
    # print(page)
    c_patten = '<div id="content">(.*)</div>'
    g = re.search(c_patten, page)
    if g:
        cc = g.group(1)
        # print(cc)
        cc = re.sub('&nbsp;', '', cc)
        cc = re.sub('<br /><br />', '\n', cc)
        # print(cc)
    return cc
    pass
 
def writeFile(dirname, filename, content):
    w_handle = codecs.open(dirname+'//'+filename+".txt", mode='wb', encoding='utf8')
    w_handle.write(content)
    w_handle.close()
    pass
 
if __name__ == '__main__':
    m = getBookMemu('http://www.biquge.la/book/14/')
    print("m",m)
    dirname='D:\Program Files\Python_Workspace\spiders\一些小例子'
    print("dirname",dirname)
    for c in m.keys():
        url = c
        name = m[c]
        print("name",name)
        print('%s, %s' %(url, name))
        while True:
            try:
                cc = getContent(url)
                # print(cc)
                if not os.path.exists('biquge'):
                    os.mkdir('biquge')
                writeFile('biquge', name, cc)
                break
            except:
                continue
    print("get book over")
