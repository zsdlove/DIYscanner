# -*- coding:utf-8 -*-
from celery import Celery
import spider
import sys
from RDB import RDB
import requests
import whois
sys.path.append('crawler')
from spiderMain import Main
from spiderMain import getdomain
app = Celery('scan',include=['spider'],backend='redis://localhost:6379/4',broker='redis://localhost:6379/5')
# 官方推荐使用json作为消息序列化方式
app.conf.update(
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_ENABLE_UTC=True,
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
)

@app.task(ignore_result=True)
def doscantask(msg):
    taskid=msg.get('taskid')
    website=msg.get('website')
    profile=msg.get('profile')
    print(u"扫描ID>>"+str(taskid))
    print(u"扫描站点>>"+website)
    print(u"扫描配置>>"+str(profile))
    print(u"开始扫描！")
    #在这里链接rdb，然后存储header信息
    try:
        rdb = RDB()
        rdb.connect()
        res=requests.get(website)
        print(res.headers)
        rdb.getheaders(str(res.headers),taskid)
        whoisinfo=whois.whois(getdomain(website))
        print(whoisinfo)
        rdb.getwhoisinfo(taskid,str(whoisinfo))
        rdb.generate_post_table(taskid)
        rdb.close()
    except:
        pass
    #Main(website)#开始爬行

