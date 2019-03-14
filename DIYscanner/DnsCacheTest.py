#coding=utf-8
'''
dnscachetest.py
http请求时，每次会先去查询下这个域名对应的ip
这是种耗时的操作。频繁的dns查询会拖慢扫描速率，所以需要改进下代码。
让每个域名只进行一次扫描。

'''
import socket
import requests
_dnscache={}
'''
针对*args和**kwargs
其中*args表示穿进来的参数存在一个元组里
func(a,b,c)
(a,b,c)
而**kwargs表示传进来的参数存在一个字典里
func(a=1,b=2,c=3)
{'a':1,'b':2,'c':3}
'''
def _setDNSCache():
    def _getaddrinfo(*args,**kwargs):
        global _dnscache
        if args in _dnscache:#如果dns缓冲中有
            return _dnscache[args]#则返回缓存中的ip
        else:#如果没有
            _dnscache[args]=socket._getaddrinfo(*args,**kwargs)#进行dns查询并将结果放入缓存中
            return _dnscache[args]
    if not hasattr(socket,'_getaddrinfo'):
        socket._getaddrinfo=socket.getaddrinfo#这里时间两个函数名进行了互换，构思很巧妙
        socket.getaddrinfo=_getaddrinfo
if __name__=="__main__":
    _setDNSCache()
    r1=requests.get("http://www.baidu.com")
    print "第一次没命中缓存的时间"+str(r1.elapsed.microseconds)
    r2=requests.get("http://www.baidu.com")
    print "第二次命中缓存的时间"+str(r2.elapsed.microseconds)