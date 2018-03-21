 
#-*-coding:utf-8-*- 
'''
Created on 2017年3月27

@author: ning.lin
'''



import datetime
import string
import time

from django import db
import ibm_db
import ibm_db_dbi
import ibm_db_django
import ibm_db_dlls
import xlwt


#maintain/OCH2012ujm
#DB2INST1
conn = ibm_db_dbi.connect("PORT=50000;PROTOCOL=TCPIP;", host="10.0.12.115",database="TRENDYEC", user="maintain",password="OCH2012ujm")
#conn = ibm_db_dbi.connect("DATABASE=DB2INST1;HOSTNAME=10.0.12.115;PORT=50000;PROTOCOL=TCPIP;UID=maintain;PWD=OCH2012ujm;", "", "")
#conn.set_autocommit(True)#设置自动提交

cursor = conn.cursor()
#sql = "select orders_id from DB2INST1.orders where orders_id='11566785'"
#result = cursor.execute(sql)
orders_id='11566785'
cursor.execute('select LASTUPDATE from DB2INST1.orders where orders_id=%s' % orders_id)
rows = cursor.fetchall()
print(rows)
def task_time(formattime):
    t1=str(formattime)[20:31]
    t2=str(formattime)[33:42]
    t=t1.replace(', ', '-')+' '+t2.replace(', ', ':')
    return t
print(task_time(rows))

workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('orders')
style = xlwt.XFStyle()
style.num_format_str = 'YY/M/D h:mm:ss' # Other options: D-MMM-YY, D-MMM, MMM-YY, h:mm, h:mm:ss, h:mm, h:mm:ss, M/D/YY h:mm, mm:ss, [h]:mm:ss, mm:ss.0
worksheet.write(0, 0, task_time(rows), style)
workbook.save('1.xls')