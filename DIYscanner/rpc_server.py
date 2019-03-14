#coding=utf-8
import spider
'''
rpc_server.py
将数据库的操作方法定义在服务端，供客户端进行调用执行
这里使用的是rpc机制
下面测试的是，调用spider方法进行扫描
'''
from rpyc import Service
from rpyc .utils.server import ThreadedServer
class RpcServer(Service):
    def exposed_test(self,url):
		print "正在接收任务请求..."
		print "正在处理任务请求..."
		print "正在进行扫描..."
		spider.oneproc(url)
		return "来自服务器zsdlove的提示：扫描结束！^_^"
s=ThreadedServer(RpcServer,port=9997,auto_register=False)
s.start()
