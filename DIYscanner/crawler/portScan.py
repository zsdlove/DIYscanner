# -- coding:utf-8 --
import threading
import requests
import time
from Queue import Queue
que=Queue(10000)
import socket
lock = threading.Lock()
class portScan(threading.Thread):
    def __init__(self, que):
        threading.Thread.__init__(self)
        self.que = que
    def run(self):
        print("Start--thread:"+self.name)
        while True:
            try:
                if que.qsize()==0:
                    break
                worker(self.que)
            except:
                break
        print("线程："+self.name+"结束~~")

'''
模块接口，供爬虫扫描器调用
'''

def startPortScan(host,ip,port):
        initportscan(host,ip,port)
        threads=[]
        for i in range(100):
            thread =portScan(que)
            thread.setDaemon(True)
            threads.append(thread)
            thread.start()
        # 同步线程，避免主线程提前终止，保证整个计时工作
        for t in threads:
            t.join()

def putIpAndPort2que(ip,startport,endport):
    for port in range(startport,endport):
        que.put(str(ip)+":"+str(port))

#主逻辑
def worker(que):
        ipandport=que.get()
        ip=ipandport.split(':')[0]
        port=ipandport.split(':')[1]
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.settimeout(3)
        try:
            server.connect((ip, int(port)))
            print('{0} port {1} is open'.format(ip,port))
        except Exception as err:
            print('{0} port {1} is not open'.format(ip, port))
        finally:
            server.close()
def initportscan(host,startport,endport):
    startport=20
    endport=1000
    putIpAndPort2que(host,startport,endport)
    print("队列初始化完毕，开始进行端口扫描")
if __name__ == '__main__':
    startPortScan("","","") #host,startport,endport

