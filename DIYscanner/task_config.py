#coding=utf-8
'''
配置任务信息
'''
class task_config:
    TASK_ID=""
    WEBSITE=""
    PROFILE=""
    MESSAGE=""
    def __init__(self,TASK_ID,WEBSITE,PROFILE,MESSAGE):
        self.TASK_ID=TASK_ID
        self.WEBSITE=WEBSITE
        self.PROFILE=PROFILE
        self.MESSAGE

    def settaskid(self,TASK_ID):
        self.TASK_ID=TASK_ID

    def setwebsite(self,WEBSITE):
        self.WEBSITE=WEBSITE

    def setprofile(self,PROFILE):
        self.PROFILE=PROFILE

    def gettaskid(self):
        return self.TASK_ID

    def getwebsite(self):
        return self.WEBSITE

    def getprofile(self):
        return self.PROFILE