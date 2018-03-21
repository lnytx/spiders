#-*-coding:utf-*-
'''
Created on 2017年4月13日

@author: ning.lin
'''
from _collections import deque
from multiprocessing import Pool
import os
from queue import Queue
import random
import threading
import time

from django.utils.functional import empty


#将url写入队列
def wqueue(url,filename):
    with open(filename,'a') as f:
        f.write(url)
        f.write('\n')
#从队列中读取url
def rqueue(filename):
    list1=[]
    with open(filename,'r') as f:
        for line in f.readlines():
            list1.append([line.strip('\n')])
        return list1
#从文件中读取数据到队列
filename="D:\\tuba\\queue.txt"
filename2="D:\\tuba\\queue2.txt"
# for i in range(1,100):
#     wqueue(str(i),filename)
def get_queue(filename):
    queue1=Queue()
    with open(filename,'r') as f:
        for line in f.readlines():
            queue1.put(line.strip('\n'))
        return queue1
#queue1=get_queue(filename)
#print(len(queue1))
# while queue1 is not empty:
#     print(queue1.get())
#定义线程池的任务函数
def thread_pool_task():
    #time.sleep(random.random() * 3)
    queue1=get_queue(filename)
    url="http://www.baidu.com//"
    str1=url+queue1.get()
    print("str1",str1)
    #调用方法，写入文件
    print(os.path.join(str1,filename2))
    wqueue(os.path.join(str1,filename2))
if __name__=='__main__':
    p = Pool(9)
    queue1=get_queue(filename)
#     while not queue1.empty():
#         print("queue.get()",queue1.get())
#         p.apply_async(thread_pool_task, args=queue1.get())
#     p.close()
#     p.join()
    while not queue1.empty():
        t1 = threading.Thread(target=thread_pool_task)
        t2 = threading.Thread(target=thread_pool_task)
        t1.start()
        t2.start()
        t1.join()
    t2.join()
    


