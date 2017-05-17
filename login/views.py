from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
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
def login(request):
    return render(request, 'login.html',{})

'''
METHOD:GET
URL:/login/loginpermit
RETURN:permit login
ASYNC:false
'''
@require_http_methods(['GET'])
def loginpermit(request):
    username=request.GET.get('username')
    passwd=request.GET.get('passwd')
    status=service.permitlogin(username,passwd)
    return HttpResponse(json.dumps({
        'status': status
    }))
