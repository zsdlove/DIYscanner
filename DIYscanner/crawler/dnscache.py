# -- coding:utf-8 --
import socket
_dnscache = {}#dns缓存list，用来记录域名和对应的IP
def _setDNSCache():
    def igetaddrinfo(*args,**kwargs):
        if args in _dnscache: #查询请求的域名是否在DNS缓存中
            return _dnscache[args]
        else:
            _dnscache[args] = socket.igetaddrinfo(*args,**kwargs)
#调用igetaddrinfo将DNS加入缓存
        return _dnscache[args]
    if not hasattr(socket, 'igetaddrinfo'):
# 将socket类的getddrinfo打一个patch，向已知DNS的方向解析
        socket.igetaddrinfo =socket.getaddrinfo
        socket.getaddrinfo = igetaddrinfo