# -- coding:utf-8 --
'''
计划使用aop编程思想进行poc测试
'''
class VulCheckEngine:
    def __init__(self, que):
        pass
        self.CustomizedPolicy=[]
        self.portRange=[]
    def loadAllVulCheckPluginName(self):
        pass

    def loadCustomizedPolicy(self):#加载自定义扫描规则
        pass

    def setCustomizedPolicy(self,CustomizedPolicy):#设置自定义扫描策略
        self.CustomizedPolicy=CustomizedPolicy

    def setPortRange(self,portRange):
        self.portRange=portRange

    def getVulPluginPath(self):
        pass
