#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import json
import global_val_model as gl
from rpyc import Service
from rpyc .utils.server import ThreadedServer
'''
这里需要保证每次启动/部署项目之前global_val_model中的参数值与task_que表中的表项数一致，
否则会重新扫描上一次的任务。最好在每次部署前将数据库初始化。
'''
class DBService(Service):
    def __init__(self):
        pass
    #数据库连接
    def exposed_open(self):
        self.__conn=MySQLdb.connect("localhost","root","root","geekscanner",charset='utf8')

    #执行sql语句
    def executeQuery(self,sql):
        cursor=None
        try:
            cursor=self.__conn.cursor()
            cursor.execute(sql)
            result=cursor.fetchall()
            self.__conn.commit()
            print "success operation"
            return result
        finally:
            if cursor != None:
                cursor.close()

    #更新数据库
    def executeUpdate(self,sql):
        cursor=None
        try:
            cursor=self.__conn.cursor()
            cursor.execute(sql)
            count=self.__conn.affected_rows()
            self.__conn.commit()
            return count
        finally:
            if cursor!=None:
                cursor.close()
    def exposed_close(self):
        self.__conn.close()

    #初始化数据库（清空）
    def exposed_initDatabase(self):
        try:
            self.exposed_open()
            sql1="truncate task_que"
            self.executeQuery(sql1)
            sql2="truncate scan_result"
            self.executeQuery(sql2)
            print("初始化数据库成功！")
        except:
            print("初始化数据库异常！")


    #获取任务
    def exposed_client_getNewtasks(self,num):
        self.exposed_open()
        sql = "select*from task_que where taskid>%d"%(int(gl.lasttaskid),)
        result = self.executeQuery(sql)
        taskcount=self.executeQuery("select count(*) from task_que")
        gl.lasttaskid=taskcount[0][0]
        print("打印记录数：")
        print(gl.lasttaskid)
        return result

#存储返回的header信息
#taskid为识别点
    def exposed_saveheaderinfo(self,headers,taskid):
        self.exposed_open()
        entry="ssd"
        result="ssd"
        whois="ssd"
        sql="insert into scan_result values(%d,%s,%s,%d,%d,%d,%d,%s,%s)"%(int(taskid),repr(entry),repr(result),4,3,2,1,repr(headers),repr(whois))
        self.executeQuery(sql)
        print("插入headers成功")
    #保存whois信息
    def exposed_savewhoisinfo(self,taskid,whois):
        self.exposed_open()
        sql = "update scan_result set whois=%s where taskid=%d"%(repr(whois),int(taskid))
        self.executeQuery(sql)
        print("插入whois成功")

    #保存POST数据包
    def exposed_savepostpackage(self,taskid,packetid,packetdata,dtime):
        self.exposed_open()
        table_name="pOny"+str(taskid)
        sql="insert into %s values(%d,%s,%s)"%(table_name,int(packetid),packetdata,dtime)
        self.executeQuery(sql)
        print("保存post包成功")

    #生成post数据存储表
    def exposed_generate_table(self,taskid):
        self.exposed_open()
        table_name="pOny"+str(taskid)
        sql = '''create table %s(
            packetid varchar(20) NOT NULL,
            packetdata TEXT,
            dtime   DATETIME
        )
        ''' % table_name
        self.executeQuery(sql)
        print("生成post存储表成功")

#这里不可用拼接，之后需要修改
    def exposed_updateFlag(self,taskid,flag):
            self.executeUpdate("update task_que set flag=%s where taskid=%s"%(flag, taskid))
            print("更新状态成功")
    def exposed_updateStart(self,taskid,taskstarttime):
            self.executeUpdate('''update task_que set starttime=%s where taskid=%s'''%('2019-01-12 12:07:00', taskid))
            print("更新时间成功")
s=ThreadedServer(DBService,port=9998,auto_register=False)
s.start()




