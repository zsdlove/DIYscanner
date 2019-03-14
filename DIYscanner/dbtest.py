# -*- coding: UTF-8 -*-
import MySQLdb
taskid="t123"
sql = '''create table %s(
    packetid varchar(20) NOT NULL,
    packetdata TEXT,
    dtime   DATETIME
)
'''%taskid
__conn=MySQLdb.connect("localhost","root","root","geekscanner",charset='utf8')
cursor = __conn.cursor()
cursor.execute(sql)
print("创建数据表成功")