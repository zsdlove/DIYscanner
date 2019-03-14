#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
自动填表功能
针对网络请求带参数情况
'''
form_name={
    'hacker':['username','user','userid','nickname','name','uname','nicheng','yonghuming'],
    'abc123456':['password','pass','pwd','passwd','mima','pword'],
    'hacker@gmail.com':['email','mail','usermail','email_address','emailAddress'],
    '13800000000':['mobile','phonenumber','phone','telephone'],
    'this is just for a test':['content','text','query','search','data','comment'],
    'www.test.com':['domain'],
    'http://ww.test.com':['link','url','website']
}
def smart_fill(variable_name):
    variable_name=variable_name.lower()#取小写字母
    flag=False
    for filled_value,variable_name_list in form_name.items():
        for variable_name_db in variable_name_list:
            if variable_name_db==variable_name:
                flag=True
                return filled_value
    if not flag:
        msg='[smart_fill]Failed to find a value for parameter with name'

if __name__=="__main__":
    print "username=%s" % smart_fill("username")
    print "password=%s" % smart_fill("password")
    print "domain=%s" % smart_fill("domain")
    print "email=%s" % smart_fill("email")
    print "content=%s" % smart_fill("content")