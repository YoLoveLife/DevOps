from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login
from django.views.decorators.http import require_http_methods
from login import service
import json
'''
METHOD:GET
URL:/login
RETURN:template of page login
ASYNC:true
'''
@require_http_methods(["GET"])
def logintest(request):
    return render(request, 'login.html',{})

'''
METHOD:GET
URL:/login/loginpermit
RETURN:permit login
ASYNC:false
'''
@csrf_exempt
@require_http_methods(['GET'])
def loginpermit(request):
    username=request.GET.get('username')
    passwd=request.GET.get('passwd')
    #status=service.permitlogin(username,passwd)
    user = authenticate(username=username,password=passwd)
    if user is not None:
        if user.is_active:
            login(request,user)
            return HttpResponseRedirect("/test/")
            '''
            return HttpResponse(json.dumps({
                 'status': '1'
              }))
            '''
        else:
            print("aaa")
    else:
        print("bbb")

@require_http_methods(['GET'])
def test(request):
    print("kkk")
    return HttpResponse(json.dumps({
        'status': '1'
    }))
