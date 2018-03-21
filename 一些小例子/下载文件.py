'''
Created on 2017年5月9日

@author: ning.lin
'''
#方法-
import urllib 

import requests
import requests 

import urllib
import urllib.request

def method1():
    print ("downloading with urllib")
    url = 'http://www.jb51.net//test/demo.zip'
    print ("downloading with urllib")
    urllib.request.urlretrieve(url, "demo.zip")
#方法二：
def method2():
    print ("downloading with urllib2")
    url = 'http://www.jb51.net//test/demo.zip'
    f = urllib.request.urlopen(url) 
    data = f.read() 
    with open("demo2.zip", "wb") as code:   
      code.write(data)
#方法三：
def method3():
    print ("downloading with requests")
    url = 'http://wangshuo.jb51.net:81/201607/books/Pythonzdhyw_jb51.rar'
    r = requests.get(url) 
    with open("demo3.zip", "wb") as code:
       code.write(r.content)
if __name__=='__main__':
    method3()