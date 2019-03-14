#coding=utf-8
'''
mitm-startup.py
启动mitmdump抓包程序
注意引入mitmproxy所在路径，否则会报路径错误
'''
import os
import sys
sys.path.append("/usr/local/bin/")
if __name__ == "__main__":
    print("启动mitmdump抓包程序")
    os.system("mitmdump -s mitm.py")


