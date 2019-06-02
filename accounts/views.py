from django.shortcuts import render
import json
from accounts import mysql
import baidu
from baidu import searchFace
from baidu import registerFace
import base64
# Create your views here.
from django.http import HttpResponse, HttpResponseForbidden
from django.http import QueryDict
from django.core import serializers
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session

ok_result = {'status':'OK'}
failed_result = {'status':'FAILED'}

#管理员登录
def admin_login(request):
    if request.method == 'GET':
        mobile = request.GET.get('mobile')
        password = request.GET.get('password')
        user = mysql.select_user(mobile,password)
        if user:
            response = HttpResponse(json.dumps(ok_result),content_type="application/json")
            request.session['user_info'] = user
            return response
        else: 
            return HttpResponseForbidden(json.dumps(failed_result),content_type="application/json")

#参会者登录
def att_login(request):
    print(request.build_absolute_uri())
    if request.method == 'POST':
        json_data = json.loads(request.body)
        loginPhoto = json_data['loginPhoto']
        # strs = loginPhoto
        # imgdata=base64.b64decode(strs)
        # file=open('1.jpg','wb')
        # file.write(imgdata)
        if json_data:
            user_id = searchFace.search(loginPhoto)
            if user_id:
                user = mysql.find_user_by_id(user_id)
                if user:
                    response = HttpResponse(json.dumps(ok_result),content_type="application/json")
                    request.session['user_info'] = user
                    return response            
        return HttpResponseForbidden(json.dumps(failed_result),content_type="application/json")


#创建会议查找
def create_meeting_list(request):
    if request.method == 'GET':
        user = request.session.get('user_info')
        if user:
            founderId = user['id']
            meetings = mysql.select_meeting(founderId)
            ret = []
            for m in meetings:
                total = mysql.meeting_total(m['id'])
                hc = mysql.meeting_hc(m['id'])
                ret.append({'start_at':m['start_at'],'end_at':m['end_at'],'name':m['name'],'id':m['id'],'founder_name':m['founder__user'], 'total':total, 'hc':hc})
            json_data = json.dumps(list(ret),cls=DjangoJSONEncoder)
            #cls use to seriallizable type datetime
            #json_data = json.dumps(list(map(model_to_dict,meetings)),cls=DjangoJSONEncoder)
            return HttpResponse(json_data,content_type="application/json")

            return HttpResponseForbidden(json.dumps(failed_result),content_type="application/json")
 


#参会会议查找
def att_meeting_list(request):
    if request.method == 'GET':
        user = request.session.get('user_info')
        userId = user['id']
        meetings = mysql.select_meeting_att(userId)
        ret = []
        for m in meetings:
            total = mysql.meeting_total(m['meeting__id'])
            hc = mysql.meeting_hc(m['meeting__id'])
            ret.append({'status':m['status'],'start_at':m['meeting__start_at'],'end_at':m['meeting__end_at'],'name':m['meeting__name'],'id':m['meeting__id'],'founder_name':m['meeting__founder__user'],'total':total,'hc':hc})
        json_data = json.dumps(list(ret),cls=DjangoJSONEncoder)
        return HttpResponse(json_data,content_type="application/json")
    
        return HttpResponseForbidden(json.dumps(failed_result),content_type="application/json")


#用户注册
def register(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        username = json_data['username']
        password = json_data['password']
        mobile = json_data['mobile']
        pic = json_data['pic']
        def upload(user_id):
             registerFace.registerFace(user_id,pic)
        userId = mysql.insert_user(username,password,mobile,upload)
        user = mysql.select_user(mobile,password)
        if userId:
            request.session['user_info'] = user
            return HttpResponse(json.dumps(ok_result),content_type="application/json")
        else: 
            return HttpResponseForbidden(json.dumps(failed_result),content_type="application/json")


#会议创建
def create(request):
    if request.method == 'POST':
        user = request.session.get('user_info')
        founderId = user['id']
        json_data = json.loads(request.body)
        name = json_data['name']
        start = json_data['start']
        end = json_data['end']
        meeting_id = mysql.insert_meeting(founderId,name,start,end)
        if meeting_id:
            ok_insert = {'meeting_id':meeting_id}
            return HttpResponse(json.dumps(ok_insert),content_type="application/json")
        else: 
            return HttpResponseForbidden(json.dumps(failed_result),content_type="application/json")

#添加会议成员
def addusers(request):
    if request.method == 'POST':
        user = request.session.get('user_info')
        json_data = json.loads(request.body)
        meetingId = json_data['meeting_id']
        userId = user['id']
        # userIds =json_data['userIds']    
        # userIds = userIds.split(",")
        if mysql.insert_users_meeting(meetingId,userId):
            return HttpResponse(json.dumps(ok_result),content_type="application/json")
        else: 
            return HttpResponseForbidden(json.dumps(failed_result),content_type="application/json")

#删除用户所在会议
def delete_users_meeting(request):
    if request.method == 'POST':
        user = request.session.get('user_info')
        userId = user['id']
        json_data = json.loads(request.body)
        meetingId = json_data['meeting_id']
        if mysql.delete_users_meeting(meetingId,userId):
            return HttpResponse(json.dumps(ok_result),content_type="application/json")
        else: 
            return HttpResponseForbidden(json.dumps(failed_result),content_type="application/json")

#删除会议
def delete_meeting(request):
    if request.method == 'POST':
        user = request.session.get('user_info')
        userId = user['id']
        json_data = json.loads(request.body)
        meetingId = json_data['meeting_id']
        if mysql.delete_meeting(meetingId):
            return HttpResponse(json.dumps(ok_result),content_type="application/json")
        else: 
            return HttpResponseForbidden(json.dumps(failed_result),content_type="application/json")

# 修改会议信息        
def update_meeting(request):
    if request.method == 'POST':
        user = request.session.get('user_info')
        userId = user['id']
        json_data = json.loads(request.body)
        meetingId = json_data['meeting_id']
        column = json_data['column']
        info = json_data['info']
        if mysql.update_meeting(column,info,meetingId):
            return HttpResponse(json.dumps(ok_result),content_type="application/json")
        else: 
            return HttpResponseForbidden(json.dumps(failed_result),content_type="application/json")

# 修改人员信息        
def update_user(request):
    if request.method == 'POST':
        user = request.session.get('user_info')
        userId = user['id']
        json_data = json.loads(request.body)
        column = json_data['column']
        info = json_data['info']
        if mysql.update_user(column,info,userId):
            return HttpResponse(json.dumps(ok_result),content_type="application/json")
        else: 
            return HttpResponseForbidden(json.dumps(failed_result),content_type="application/json")



#修改参会状态
def update_user_meeting(request):
    if request.method == 'POST':
        user = request.session.get('user_info')
        userId = user['id']
        json_data = json.loads(request.body)
        status = json_data['status']
        meetingId = json_data['meeting_id']
        if mysql.update_user_meeting(status,meetingId,userId):
            return HttpResponse(json.dumps(ok_result),content_type="application/json")
        else: 
            return HttpResponseForbidden(json.dumps(failed_result),content_type="application/json")




#摄像头拍摄修改用户参会状态
def update_user_status(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        meeting_id = json_data['meeting_id']
        status = json_data['status']
        user_id = json_data['user_id']
        if mysql.update_user_meeting(status,meeting_id,user_id):
            return HttpResponse(json.dumps(ok_result),content_type="application/json")
        else: 
            return HttpResponseForbidden(json.dumps(failed_result),content_type="application/json")


    





