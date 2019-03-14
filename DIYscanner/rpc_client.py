#coding=utf-8
'''
rpc_client
从服务端远程调用对象，获取任务队列，然后执行任务
'''
import rpyc
c=rpyc.connect('localhost',9999)
print c.root.test("http://testphp.vulnweb.com")
c.close()