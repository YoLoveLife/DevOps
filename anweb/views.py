from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from anweb import service
import json
'''
METHOD:GET
URL:/anweb
RETURN:template of page index
ASYNC:true
'''
@require_http_methods(["GET"])
def index(request):
    return render(request, 'index.html',{})

'''
METHOD:GET
URL:/anweb/groupsearch
RETURN:list of group by json
ASYNC:false
'''
@require_http_methods(["GET",])
def groupsearch(request):
    list=service.group9groupsearch()
    return HttpResponse(json.dumps({
        'group_list': list
    }))

'''
METHOD:POST
URL:/anweb/groupmodify
RETURN:modify the group data if the group don't exsit add this group to database
ASYNC:true
'''
@csrf_exempt
@require_http_methods(["POST"],)
def groupmodify(request):
    group_id=request.POST.get('groupid')
    group_name=request.POST.get('groupname')
    group_remark=request.POST.get('groupremark')
    service.group9modifygroup(group_id,group_name,group_remark)
    return HttpResponse(json.dumps({
        'status': "1"
    }))

'''
METHOD:GET
URL:/anweb/hostsearch
POST:groupid
RETURN:list of host for groupid
ASYNC:false
'''
@csrf_exempt
@require_http_methods(["GET"],)
def hostsearch(request):
    group_id=request.GET.get('group_id')
    list=service.host9hostsearch(group_id)
    return HttpResponse(json.dumps({
        'host_list': list
    }))

'''
METHOD:GET
URL:/anweb/softversion
POST:app_id
RETURN:list of app version
ASYNC:false
'''
@csrf_exempt
@require_http_methods(["GET"],)
def softversion(request):
    appname=request.GET.get('appname')
    list=service.batch9appversion(appname)
    print(list)
    return HttpResponse(json.dumps({
        'host_list': list
    }))

'''
METHOD:POST
URL:/anweb/batchtomcat
POST:list of tomcat install info
RETURN:true/false
ASYNC:true
'''
@csrf_exempt
@require_http_methods(["POST"],)
def batchtomcat(request):
    iplist=request.POST.getlist('iplist[]')
    javaversion=request.POST.get('javaversion')
    tomcatversion=request.POST.get('tomcatversion')
    javaprefix=request.POST.get('javaprefix')
    tomcatprefix=request.POST.get('tomcatprefix')
    status=service.batch9tomcatinstall(iplist,javaversion,javaprefix,tomcatversion,tomcatprefix);
    return HttpResponse(json.dumps({
        'status': status
    }))

'''
METHOD:POST
URL:/anweb/batchmysql
POST:list of mysql install info
RETURN:true/false
ASYNC:true
'''
@csrf_exempt
@require_http_methods(["POST"],)
def batchmysql(request):
    iplist = request.POST.getlist('iplist[]')
    mysqlversion = request.POST.get('mysqlversion')
    mysqlprefix = request.POST.get('mysqlprefix')
    mysqlpasswd=request.POST.get('mysqlpasswd')
    status=service.batch9mysqlinstall(iplist,mysqlversion,mysqlprefix,mysqlpasswd)
    return HttpResponse(json.dumps({
        'status': status
    }))