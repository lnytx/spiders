'''
Created on 2018年2月28日

@author: ning.lin
'''
def consumer():
    r = ''
    while True:
        print("r1",r)
        n = yield r+'sdfasfasf'#n是c.send()发送的值,当前表达式里的值，r只是加了个字符串
        print("n1",n,type(n))
        print("r2",r)
        if not n:
            print("not n",n)
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'

def produce(c):
    c.send(None)#next(c)第一次不能有数据发过去，否则会报错，只能是None
    print("c",c)
    n = 0
    while n < 5:
        n = n + 1
        print("n++",n)
        print('[PRODUCER] Producing %s...' % n)
        r = c.send('sssssssssssssssssss')
        print("r",r)#这里的r是返回的yield关键字后的r+'sdfasfasf'
        print("nn",n)
    c.close()

c = consumer()
produce(c)