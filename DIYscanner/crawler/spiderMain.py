# -- coding:utf-8 --
'''
@author:Pony@moresec.com
@time:2018.12.16
'''
import socket
import threading
import requests
import time
from Queue import Queue
from bs4 import BeautifulSoup
import urllib
from SpiderConfig import SpiderConfig
import dnscache
dnscache._setDNSCache()  # 启用dns缓存
import portScan
import urlparse
import sys
sys.path.append('plugins')
from sqli import check
import os
#线程锁
lock = threading.Lock()
spiderconf = SpiderConfig()

'''
Mutiple Threads SuperSpider
'''

'''
load plugins
'''
def loadplugins(file_dir):#plugins
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.py':
                L.append(file+".py")
    return L
class SuperSpider(threading.Thread):
    def __init__(self, que):
        threading.Thread.__init__(self)
        self.que = que

    def run(self):
        print("Start--thread:"+self.name)
        while True:
            try:
                crawler(self.que)
            except:
                break
        print("线程："+self.name+"结束~~")


#下载页面内容
def download(url):
    flag=True
    while(flag):
        try:
            if spiderconf.getproxystatus():#判断是否启用了代理
                res=requests.get(url,timeout=4,proxies=spiderconf.getproxy(),cookies=spiderconf.getcookie())
                flag=False
            else:
                res=requests.get(url,timeout=4,cookies=spiderconf.getcookie())
                flag=False
                #要智能点，可以在这里加一个403判断，如果status_code是403则启用代理
        except:
           # spiderconf.setproxy(getproxy())#切换代理
            continue
    return res

'''
format url
'''
def format(url):
    urlformat=urlparse.urlsplit(url)
    netloc=urlformat[1]
    path=urlformat[2]
    query=urlformat[3]
    temp=(netloc,tuple([len(i) for i in path.split('/')]),tuple(sorted([i.split('=')[0] for i in query.split('&')])))
    return temp
'''
test==>http://www.baidu.com/zsdlove/hello/fuck?talk=1&nice=sldk&like=nnnsd2
format==>('www.baidu.com', (0, 7, 5, 4), ('like', 'nice', 'talk'))
similar julging==>similar_set   a global set
'''

'''
去相似url
'''
def IsSimilarURL(url):
    urlformat=format(url)
    if urlformat not in spiderconf.similar_set:
        spiderconf.similar_set.add(urlformat)
        return True
    else:
        return False
    return False


def saveurl(newurl):
    if newurl.endswith('xml') or newurl.endswith('pom'):
        res = download(newurl)
        spiderconf.getsavefile().write(newurl + "\n")
        spiderconf.getsavefile().write(res.text + "\n")

#往队列里添加url
def doqueput(urls,que):
    for  newurl in urls:
        if IsSpidered(newurl) and IsOverDeep(newurl):
            saveurl(newurl)#保存xml和pom结尾文件，后期可以增加图片等
        if IsSpidered(newurl) and IsOverDeep(newurl):
            putURL2que(que,newurl)
            spiderconf.oldurl.append(newurl)
            print("已经爬取"+str(len(spiderconf.oldurl))+"条连接")
            print("将新url放到que中：" + newurl)
            print("队列大小:"+str(que.qsize()))

def flaws_detection_engine(urls):
    for url in urls:
        check(url)
#往队列里添加url
def putURL2que(que,newurl):
    que.put(newurl)
# 解析url，放入队列
def parseURL(que, urls):
    doqueput(urls,que)

def getdomain(url):
    domain=urlparse.urlsplit(url)[1]
    return domain

def getNewUrl(que):
    url=''
    with lock:
            flag=True
            while(flag):#直到取出的是没有爬取过的
                tmp = que.get(timeout=3)
                if IsSimilarURL(tmp):
                    url=tmp
                    flag=False
    return url
def crawler(que):
            baseurl=getNewUrl(que)
            check(baseurl)
            content = download(baseurl).content
            soup = BeautifulSoup(content, 'html.parser')
            AllHrefTag1 = soup.find_all('a')
            AllHrefTag2=soup.find_all('A')
            AllHrefTag=AllHrefTag1+AllHrefTag2
            newurls = []
            for hreftag in AllHrefTag:
                 try:
                       url = str(hreftag['href'])
                       if "http:" in url and isinnerurl(url):
                           newurls.append(url)
                       elif "https:" in url and isinnerurl(url):
                           newurls.append(url)
                       elif url.startswith('/'):
                           newurls.append(baseurl+url)
                 except:
                   continue
            newurls=set(newurls)
            parseURL(que, newurls)

#判断是否是已经爬取
def IsSpidered(url):
    if url in spiderconf.oldurl:
        return False
    else:
        return True
    return True

#判断是否是当前域内的URL
def isinnerurl(url):
    urldata=urlparse.urlsplit(url)
    if spiderconf.getdomain()==urldata[1]:
        return True
    else:
        return False
    return True

#URL净化
def urlclean(url):
    pass

'''
判断是否超过设定的爬行深度
'''
def IsOverDeep(url):
    urldata=urlparse.urlsplit(url)
    SplitResult=str(urldata[2]).split('/')
    spiderdeep=len(SplitResult)-1
    #print("目前爬行深度："+str(spiderdeep))
    if  spiderdeep>=spiderconf.getdeep():
        return False
    else:
        return True
    return True

# 获取代理
def getproxy():
    flag = True
    ipdic = {'http': 'http://119.114.125.253:58424'}
    while (flag):
        try:
            res = requests.get('http://api.ip.data5u.com/dynamic/get.html?order=4a2c1091b15515eff96cadddf0228a16&sep=6',timeout=5)
            # res=requests.get('http://dps.kdlapi.com/api/getdps/?orderid=994460608536855&num=1&pt=1&ut=1&sep=4',timeout=3)
            ip = res.text.replace(";", "").replace("\n", "").replace("|", "")
            ipdic = {'http': 'http://' + ip}
            print(ipdic)
            flag = False
        except:
            continue
    return ipdic

'''
平衡线程池,not used,bak
'''
def BalanceThreadsPool(SpiderConfig):
    if len(SpiderConfig.getthreadspool())<SpiderConfig.getthreadsNum():
        addtionalThreadsNum=SpiderConfig.getthreadsNum()-len(SpiderConfig)
        for i in range(addtionalThreadsNum):
            thread = SuperSpider(spiderconf.getque())
            thread.setDaemon(True)
            thread.start()
            thread.join()
            spiderconf.addthread(thread)

def startspider():
    for i in range(spiderconf.getthreadsNum()):
        thread = SuperSpider(spiderconf.getque())
        thread.setDaemon(True)
        thread.start()
        spiderconf.addthread(thread)
    # 同步线程，避免主线程提前终止，保证整个计时工作
    for t in spiderconf.getthreadspool():
        t.join()

#获取目标域名的ip地址
def gettargetIP(domain):
    result = socket.getaddrinfo(domain, None)
    print(result[0][4][0])
    targetip=result[0][4][0]
    return result

#爬虫主函数
def Main(url):
    '''
    爬虫全局配置
    '''
    spiderconf.setdomain(getdomain(url))  #设置域名
    spiderconf.setdeep(5)                 #设置爬行深度
    spiderconf.setque(100000)             #设置队列大小
    spiderconf.setthreadsNum(20)           #设置线程数量
    spiderconf.getque().put(url)          #将域名push到队列中
    spiderconf.setproxyswitch(False)       #打开/关闭代理，默认是关闭
    #spiderconf.setproxy(getproxy())       #设置代理
    spiderconf.setcookie('')               #设置cookie，用于登陆扫描
    spiderconf.setportrange([20,1000])
    #portScan.startPortScan(gettargetIP(spiderconf.getdomain()),spiderconf.getstartIP(),spiderconf.getendIP())端口扫描
    startspider()                         #开始扫描
    spiderconf.setfinishedtime(time.time())
    # 输出时间并结束
    print("The total time is:", spiderconf.getfinishedtime() - spiderconf.starttime)

if __name__ == '__main__':
   Main('http://www.freebuf.com')
   print(len(spiderconf.oldurl))
