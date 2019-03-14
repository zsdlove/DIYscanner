#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
用于控制扫描的速度
有点难以理解，之后再说吧
代码部分有问题，需要调试

'''
import socket
import time
import requests
def _hook_manager(_time,begin,_conn):
    def _hook_connect(*args,**kwargs):
        realfun,realargs,realkwargs=args
        while True:
            begin=time.time
            now_time=max(0.01,begin-_time)
            if now_time>5:#也就是距离上一次执行过去了5秒钟
                _conn=0
                break
            if _conn/now_time<=_speed:
                break
            else:
                time.sleep(0.01)
        _conn+=1
        return apply(realfun,realargs,realkwargs)
    _connect=socket.socket.connect
    socket.socket.connect=lambda *args,**kwargs:apply(_hook_connect,(_connect,args,kwargs))

if __name__=="__main__":
    _speed=200
    _conn=0
    _time=time.time()
    for x in xrange(0,10):
        _hook_manager(_time,_conn)
        res=requests.get('http://www.baidu.com',timeout=5)
        _time=time.time()
        print res
