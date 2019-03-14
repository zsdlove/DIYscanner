#coding=utf-8
'''
taskschedule.py
任务调度
'''
import rpyc
from Queue import Queue
from RDB import RDB
import datetime
from scan import doscantask
import time
q=Queue(1000)
if __name__ == "__main__":
    initrdb=RDB()
    initrdb.connect()
    initrdb.initDB()#初始化数据库
    initrdb.close()
    while(True):
        rdb=RDB()
        rdb.connect()
        tasks=rdb.getnewtasks()
        for task in tasks:
            msg=task.get('msg')
            print(msg)
            taskid=task.get('taskid')
            starttime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(starttime)
            rdb.updateFlag(taskid,"2")
            #rdb.updatestarttime(taskid,starttime)
            q.put(msg)
        rdb.close()
        while q.empty()==False:
            print("=")
            time.sleep(1)
            msg_list=[]
            for i in range(0,1):
                    msg=q.get()
                    print("从队列中取得msg：")
                    print(msg)
                    msg_list.append(msg)
            for item in msg_list:
                doscantask.delay(item)
        time.sleep(3)
        print("休息3s")

