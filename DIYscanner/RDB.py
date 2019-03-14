#coding=utf-8
'''
rpc_client
从服务端远程调用对象，获取任务队列，然后执行任务
'''
import rpyc
from task_config import task_config
import json
import datetime
class RDB:
    def __init__(self):
        self.client=None

    def connect(self):
        try:
            self.client=rpyc.connect('localhost',9998)
        except:
            pass
    def close(self):
        if self.client is not None:
            try:
                self.client.root.close()
            except:
                pass
            self.client.close()
        else:
            self.client=None
    def getnewtasks(self):
        data=[]
        task_queue=self.client.root.client_getNewtasks(1)
        for task in task_queue:
            msg={"taskid":task[0],"website":task[2],"profile":task[3]}
            content={"taskid":task[0],"msg":msg}
            data.append(content)
        return data

    def updateFlag(self,taskid,flag):
        self.client.root.updateFlag(taskid,flag)

    def updatestarttime(self,taskid,taskstarttime):
        self.client.root.updateStart(taskid,taskstarttime)
    #获取header信息
    def getheaders(self,headers,taskid):
        self.client.root.saveheaderinfo(headers,taskid)
    #获取whois信息
    def getwhoisinfo(self,taskid,whois):
        self.client.root.savewhoisinfo(taskid,whois)
    #初始化数据库
    def initDB(self):
        self.client.root.initDatabase()

    #保存mitm抓取的流量
    def save_postpacket(self,taskid,packetid,packetdata,dtime):
        self.client.root.savepostpackage(taskid,packetid,packetdata,dtime)

    #生成数据表
    def generate_post_table(self,taskid):
        self.client.root.generate_table(taskid)
if __name__=="__main__":
    rdb=RDB()
    rdb.connect()
    tasks=rdb.getnewtasks()
    for task in tasks:
        print(task.get('msg'))
        taskid=task.get('taskid')
        starttime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(starttime)
        rdb.updateFlag(taskid,"2")
        #rdb.updatestarttime(taskid,starttime)