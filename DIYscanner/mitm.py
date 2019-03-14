# -*- coding: utf-8 -*-
from mitmproxy import ctx
import datetime
# 所有发出的请求数据包都会被这个方法所处理
# 所谓的处理，我们这里只是打印一下一些项；当然可以修改这些项的值直接给这些项赋值即可
'''
执行命令：mitmdump -s mimt
'''
def request(flow):
    packet_file = open("packet.json", 'a+')
    # 获取请求对象
    request = flow.request
    # 实例化输出类
    info = ctx.log.info
    url=request.url.split('.')[-1]
    if url!='js' and url!='css':
        if request.method=="GET":
            pass
        elif request.method=="POST":
            info("####################################")
            info(request.method+" "+request.url)#1
            status=request.method+" "+request.url
            packet_file.write("####################################\n")
            packet_file.write(status + "\n")
            headers=request.headers#2
            for key,value in headers.items():
                info(key+":"+value)
                packet_file.write(key+":"+value+ "\n")
            info(str(request.text))#3
            packet_file.write(request.text+"\n")
            packet_file.write("####################################\n")
            info("####################################")
# 所有服务器响应的数据包都会被这个方法处理
# 所谓的处理，我们这里只是打印一下一些项
'''
def response(flow):
    # 获取响应对象
    response = flow.response
    # 实例化输出类
    info = ctx.log.info
    # 打印响应码
    info("####################################")
    info(str(response.http_version+" "+str(response.status_code)))
    # 打印所有头部
    headers=response.headers
    for key,value in headers.items():
        info(str(key)+":"+str(value))
    # 打印响应报文内容
    info(str(response.text))
    info("####################################")
'''
