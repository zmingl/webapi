from django.shortcuts import render
import json
from accounts import mysql
# Create your views here.

from django.http import HttpResponse, HttpResponseForbidden


def index(request):
    ok_result = {'status':'OK'}
    failed_result = {'status':'FAILED'}
    if request.method == 'POST':
        print(request)
        account = request.POST.get('account', '')
        password = request.POST.get('password','')
        print(account,password)
        
        if verify(account,password):
            return HttpResponse("You login successfully!")
        else: 
            return HttpResponseForbidden()

    elif request.method == 'GET':
        account = request.GET.get('account')
        password = request.GET.get('password')
        if verify(account,password):
            return HttpResponse(json.dumps(ok_result),content_type="application/json")
        else: 
            return HttpResponseForbidden(json.dumps(failed_result),content_type="application/json")


def verify(account,password):

    if mysql.select(account,password):
        # print("row:"+str(mysql.select(account,password)))
        return True
    else:
        # print("row:"+str(mysql.select(account,password)))
        return False
