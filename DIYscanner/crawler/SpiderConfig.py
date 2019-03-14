# -- coding:utf-8 --
from Queue import Queue
import time
import requests
'''
@author:Pony@moresec.com
@time:2018.12.16
配置清单：
配置队列大小
配置爬行深度
配置域名
配置线程数
blabla
'''
class SpiderConfig:

    def __init__(self):
        self.que='' #队列长度

        self.deep='' #爬行深度

        self.domain='' #域名

        self.threadsNum='' #线程数

        self.oldurl=[] #已爬取的url

        self.starttime=time.time() #开始时间

        self.finishedtime='' #结束时间

        self.threadspool=[]

        self.proxy=''

        self.savefile=open('savefile.txt','a+')

        self.proxyswitch=False

        self.similar_set=set()

        self.cookie=''

        self.targetip=""

        self.portrange=[]

        self.headers=[]

    def setportrange(self,portrange):
        self.portrange=portrange

    def setcookie(self,cookie):#设置cookie
        self.cookie=cookie

    def setproxyswitch(self,bol):
        self.proxyswitch=bol

    def setproxy(self,proxy):
        self.proxy=proxy

    def addthread(self,thread):#添加一个线程
        self.threadspool.append(thread)

    def setfinishedtime(self,finishedtime):
        self.finishedtime=finishedtime

    def setque(self,quesize):
        que=Queue(quesize)
        self.que=que

    def setoldurl(self,newurl):
        self.oldurl.append(newurl)

    def setdeep(self,deep):
        self.deep=deep

    def setdomain(self,domain):
        self.domain=domain

    def setthreadsNum(self,threadsNum):
        self.threadsNum=threadsNum

    def getcookie(self):
        return self.cookie

    def getthreadspool(self):
        return self.threadspool

    def getfinishedtime(self):
        return self.finishedtime

    def getque(self):
        return self.que

    def getdeep(self):
        return self.deep

    def getoldurl(self):
        return self.oldurl

    def getdomain(self):
        return self.domain

    def getthreadsNum(self):
        return self.threadsNum

    def getproxy(self):
        return self.proxy

    def getsavefile(self):
        return self.savefile

    def getproxystatus(self):
        return self.proxyswitch

    def getstartIP(self):#获取端口范围
        return self.portrange[0]

    def getendIP(self):
        return self.portrange[1]

