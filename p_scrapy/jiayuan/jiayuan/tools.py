# -*- coding:utf-8 -*-
'''
Created on 2018年2月28日
@author: ning.lin
'''
'''
操作代理IP表proxy_ip的，集成到tool.py中
操作包括，随机获取验证好的代理IP，修改IP状态（失效），当然也可以重新验证忆失效IP
更换代理时修改当前IP为已使用
'''
#定义几个全局变量

import datetime
import random
import time

import pymysql

from get_proxy_ip import main


def connect():
    config={'host':'127.0.0.1',
                'user':'root',
                'password':'root',
                'port':3306,
                'database':'jiayuan',
                'charset':'utf8',
                #要加上下面一行返回的是list，否则默认返回的是tuple
                'cursorclass':pymysql.cursors.DictCursor,
            }
    try:
        conn=pymysql.connect(**config)
        print("conn is success!")
        return conn
    except Exception as e:
        print("conn is fails{}".format(e))











def get_random_ip(change_ip=0):
    conn=connect()
    cursor=conn.cursor()
    now_time = time.strftime("%Y-%m-%d %H:%M:%S")
    if change_ip==0:#未传入change_ip说明是爬虫第一次开始，默认随机获取IP，不是更改IP
        try:
            rand_ip_slq = '''SELECT ip_port FROM proxy_ip WHERE id >= \
                        ((SELECT MAX(id) FROM proxy_ip)-(SELECT MIN(id ) \
                        FROM proxy_ip)) * RAND() + (SELECT MIN(id) FROM proxy_ip)  LIMIT 1
            '''
            cursor.execute(rand_ip_slq)
            ip_exit = cursor.fetchone()
            print("ip_exit",ip_exit)
            if ip_exit:
               #将当前获取的IPcurrent状态改为1并且修改当前时间为最近一次使用时间
                cursor.execute('''update proxy_ip set is_current=%s,last_time_use=%s where ip_port=%s''',(1,now_time,ip_exit['ip_port']))
            else:
                print("未找到sql该表可能为空，需要去爬IP")
                main()#从网上获取IP并写入数据库中
        except Exception as e:
            print("执行sql异常",str(e))
        finally:
            conn.commit()
            conn.close()
    else:#更改代理IP
        try:
            rand_ip_slq = '''SELECT ip_port FROM proxy_ip WHERE id >= \
                        ((SELECT MAX(id) FROM proxy_ip)-(SELECT MIN(id ) \
                        FROM proxy_ip)) * RAND() + (SELECT MIN(id) FROM proxy_ip)  LIMIT 1
                        '''
            cursor.execute(rand_ip_slq)
            ip_exit = cursor.fetchone()
            print("ip_exit2",ip_exit)
            if ip_exit:
               #将当前获取的IPcurrent状态改为1表示当前在使用的IP并且修改当前时间为最近一次使用时间
                cursor.execute('''update proxy_ip set is_current=%s,last_time_use=%s where ip_port=%s''',(1,now_time,ip_exit['ip_port']))
                #将之前状态为当前IP的状态改成0（非当前IP）
                cursor.execute("select last_time_use from proxy_ip where ip_port=%s",change_ip)
                use_time = cursor.fetchone()['last_time_use']
                startTime= datetime.datetime.strptime(str(use_time),"%Y-%m-%d %H:%M:%S")  
                endTime= datetime.datetime.strptime(str(now_time),"%Y-%m-%d %H:%M:%S")
                seconds = (endTime- startTime).seconds#获取此次与上次时间之差就等于使用了的时间
                cursor.execute('''update proxy_ip set is_current=%s,use_times=%s where ip_port=%s''',(0,seconds,change_ip))
                #cursor.execute('''update proxy_ip set is_current=%s,last_time_use=%s where ip_port=%s''',(1,now_time,ip_exit['ip_port']))
            else:
                print("未找到sql该表可能为空，需要去爬IP")
#                 main()#从网上获取IP并写入数据库中
        except Exception as e:
            print("未找到sql该表可能为空，需要去爬IP",str(e))
#             main()#从网上获
        finally:
            conn.commit()
            conn.close()
    return ip_exit['ip_port']#返回格式165.227.40.248:3128
        
def get_proxy_ip():
    '''
    scrapy通过些函数获取is_current状态为1的IP为代理IP，防止一次request换一次IP（因为登录情况下不可能出现这种情况）
    '''
    conn=connect()
    cursor=conn.cursor()
    try:
        cursor.execute("select ip_port from proxy_ip where is_current=1")
        pro_ip = cursor.fetchone()['ip_port']
    except Exception as e:
        print("get_proxy_ip报错",str(e))
    finally:
            conn.commit()
            conn.close()
    return pro_ip
        
if __name__=="__main__":
    get_random_ip()
#     check_url()
