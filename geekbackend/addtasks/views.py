# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.shortcuts import render,render_to_response
from addtasks.models import task_que
from addtasks.models import assert_info
import datetime
from addtasks.models import scan_result
import time
import json
from django.contrib import auth
from addtasks.forms import loginform
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from geekbackend import settings
import os
import sys
reload(sys)
import requests
sys.setdefaultencoding('utf8') # 设置默认编码格式为'utf-8'
#添加auth_user用户
#user = User.objects.create_user(username="root", email="747289639@qq.com", password="123456")
#user.save()
def apk_security_check(request):
	if request.method=="POST":
		file_obj=request.FILES.get("file")
		if file_obj.name.split('.')[-1]=="apk":
			f=open(os.path.join(settings.BASE_DIR,'static','APK',file_obj.name),'w')
			for chunk in file_obj.chunks():
				f.write(chunk)
			return render(request,'android_staticscan.html',{"warming":"APK文件上传成功！"})
		else:
			print("请上传.apk格式文件！")
			return render(request,"android_staticscan.html",{"warming":"请上传.apk格式文件"})
	return render(request,"android_staticscan.html")


#渲染踩点模块
@login_required(login_url='login.html')
def StepOnTheSpot(request):
	return render(request,'StepOnTheSpot.html')

#展示首页
@login_required(login_url='login.html')
def render_showgeekpage(request):
	return render(request,'geekpage.html')

#主机安全风险检测页面渲染
@login_required(login_url='login.html')
def render_HostSec(request):
	return render(request,'Host_Security_Scan.html')


#渲染android静态扫描页面
@login_required(login_url='login.html')
def render_android(request):
	return render(request,'android_staticscan.html')


#登录校验
def login(request):
	if request.method=="GET":
		#login_form=loginform(request.POST)
		hashkey = CaptchaStore.generate_key()
		image_url = captcha_image_url(hashkey)
		return render(request,"login.html",{"hashkey":hashkey,"image_url":image_url})
	elif request.method=="POST":
		uf = loginform(request.POST)
		if uf.is_valid():
			username = request.POST.get("username")
			password = request.POST.get("password")
			print(username+":"+password)
			user = auth.authenticate(username=username, password=password)
			print(user)
			if user is not None:
				auth.login(request, user)
				print("=====")
				return render(request,'index.html')
	return render(request,'login.html')

#退出登录
@login_required(login_url='login.html')
def logout_action(request):
	logout(request)
	return render(request,'login.html')

#渲染首页
@login_required(login_url='login.html')
def index(request):
	taskinfo=task_que.objects.all()
	return render(request,"index.html",{'taskList':taskinfo})

@login_required(login_url='login.html')
#渲染添加任务页面
def showaddtaskspage(request):
	return render(request,"addtasks2.html")

#渲染应急响应界面
@login_required(login_url='login.html')
def showemergencyresp(request):
	return render(request,'emergencyresp.html')


#渲染任务信息展示页面
@login_required(login_url='login.html')
def show_task_info(request):#这里应该获得一个taskid的值，通过get方法
	headers=''
	try:
		reqpath=request.path
		taskid=reqpath.split('-')[-1]#获得taskid
		print("taskid:"+taskid)
		Base_webste_info=scan_result.objects.get(taskid=taskid)
		print(Base_webste_info.headers)
		print(Base_webste_info.whois)
		whoisinfo=json.loads(Base_webste_info.whois.decode('utf-8').replace("'","\""))
		headers=json.loads(Base_webste_info.headers.decode('utf-8').replace("'","\""))
		return render(request,"show_task_info.html",{'data':headers,'whoisinfo':whoisinfo})
	except:
		time.sleep(0.2)
		return render(request, "show_task_info.html", {'data': headers})
	return render(request, "show_task_info.html", {'data': headers,'whoisinfo':whoisinfo})

#个人说明
@login_required(login_url='login.html')
def aboutme(request):
	return render(request,"aboutme.html")

#未实现
@login_required(login_url='login.html')
def unrealized(request):
	return render(request,"unrealized.html")

#系统配置设置
@login_required(login_url='login.html')
def set_sysconfig(request):
	return render(request,"sysconfig.html")

#测试
@login_required(login_url='login.html')
def test(request):
	return render(request,"test.html")

#渲染录入资产信息页面
@login_required(login_url='login.html')
def assert_entry(request):
	return render(request,"assert_entry.html")

#处理资产录入
@login_required(login_url='login.html')
def handle_newassert_entry(request):
	if request.method=='POST':
		assertdata=request.POST.get('target_urls')
		assert_name=request.POST.get('assert_name')
		assert_desc=request.POST.get('assert_desc')
		print(assertdata)
		assertArray=assertdata.split()
		assert_dicdata=str({"assert":assertArray})
		print(assertArray)
		assertdata="录入成功，以下是成功录入的资产:"+assertdata
		assert_new=assert_info(
			None,
			assert_name,
			assert_dicdata,
			assert_desc,
		)
		assert_new.save()
		return render(request, 'assert_entry.html', {"data": assertdata})


#处理任务添加
@login_required(login_url='login.html')
def handlenewtasks(request):
	if request.method=='POST':
		print('打印target_url')
		print(request.POST.get('target_url'))
		target_url=request.POST.get('target_url')
		task_name=request.POST.get('task_name')
		inque_dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		start_dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		finish_dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		datainfo="添加任务成功，待检测url是："+target_url
		#添加新任务
		task=task_que(
			None,#taskid,自增加
			task_name,#taskname
			target_url,#website
			'test',
			inque_dt,
			start_dt,
			finish_dt,
			'1',
			'1',
			'1',
			'1',
		)
		task.save()
		return render(request,'addtasks2.html',{"data":datainfo})
