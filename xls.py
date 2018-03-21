# -*- coding:utf-8 -*- 
import mysql.connector
import xlwt
from datetime import datetime
from pip._vendor.requests.packages.urllib3.connectionpool import xrange

def connect():
    config={'host':'10.1.1.174',
                'user':'zabbix',
                'password':'Zabbix2015',
                'port':3306,
                'database':'zabbix',
                'charset':'utf8'
            }
    try:
        conn=mysql.connector.connect(**config)
        return conn
        print("conn is success!")
    except mysql.connector.Error as e:
        print("conn is fails{}".format(e))
        
conn=connect();
cursor=conn.cursor()
sql='show tables'
#sql_select='select itemid,from_unixtime(clock),value,ns from history_str where itemid=%s'
sql_select='select itemid,clock,value,ns from history_str where itemid=%s'
cursor.execute(sql_select,(173562,))
# 由于查询语句仅会返回受影响的记录条数并不会返回数据库中实际的值，所以此处需要fetchall()来获取所有内容。
result=cursor.fetchall()

# 实例化一个Workbook()对象(即excel文件)
wbk = xlwt.Workbook(encoding='utf-8', style_compression=0)
# 新建一个名为Sheet1的excel sheet。此处的cell_overwrite_ok =True是为了能对同一个单元格重复操作。
sheet = wbk.add_sheet('sheet 1', cell_overwrite_ok=True)

dateFormat = xlwt.XFStyle()

dateFormat.num_format_str = '%Y-%m-%d %H:%M:%S'

row1=sheet.row(1)
print(result)
for i in xrange(len(result)):
    for j in xrange(len(result[i])):
# #将datetime.datetime(2017, 3, 14, 17, 10, 43)转换成日期格式
        print(datetime.fromtimestamp(result[i][1]))
        sheet.write(i,j,result[i][j])
wbk.save('D:\zabbix.xls')
