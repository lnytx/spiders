
import http.cookiejar
import urllib.request


#声明一个CookieJar对象实例来保存cookie
cookie=http.cookiejar.CookieJar()
#利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
handler=urllib.request.HTTPCookieProcessor(cookie)
#通过handler来构建opener
opener=urllib.request.build_opener(handler)
#此处的open方法同urllib2的urlopen方法，也可以传入request
h='User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
post_dict={
    '_ydclearance':12,
    'a':a,
    'Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31':1491812144,
    'Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31':1491812973,
    'channelid':0,
    'sid':1491814518212705
}
a=2
postDict2={
    '_xsrf':_xsrf-123,
    'email':id,
    'password':password,
    'remeberme':'y'
    }
response = opener.open('http://www.kuaidaili.com/proxylist/2/',h)
for item in cookie:
    print ('Name = '+item.name)
    print ('Value = '+item.value)