'''
Created on 2017��4��7��

@author: ning.lin
简单使用BeautifulSoup
'''
import re
import urllib.request

from bs4 import BeautifulSoup


url='http://tieba.baidu.com/index.html'
# headers={ 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0' }
# req=urllib.request.Request(url=url,headers=headers)
# html=urllib.request.urlopen(req)
# data=html.read()
page=urllib.request.urlopen(url)
html = page.read().decode('utf-8')
soup=BeautifulSoup(html,'html.parser')
#print(soup)
#for link in soup.find_all('div'):
#    print(link.get('class'))
print(soup.title.name)
print(soup.title.string)
print(soup.title.parent.name)
print(soup.div)
#print(soup.contents)#content方法 根据文档树进行搜索，返回标记对象（tag）的列表
print(soup.contents[1])
'''
findAll(name, attrs, recursive, text, limit, **kwargs)
接受一个参数，标记名
寻找文档所有 P标记，返回一个列表
'''
#print(soup.findAll('img'))
#查找对应的tag
'''
def find_all(self, name=None, attrs={}, recursive=True, text=None,  
                 limit=None, **kwargs):  

看参数。
第一个是tag的名称，第二个是属性。第3个选择递归，text是判断内容。limit是提取数量限制。**kwargs 就是字典传递了。。
'''
# for a in soup.findAll(re.compile('')):
#     print("tag name",a)
#     


#使用strings属性会返回soup的构造1个迭代器，迭代tag对象下面的所有文本内容
# for string in soup.strings:  
#     print(repr(string))  
    

#.contents会以列表形式返回tag下的节点。
head_tag=soup.head
print("head_tag",head_tag)