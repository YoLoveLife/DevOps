import json

from django.contrib.auth import authenticate,login
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from apps.anweb import service


@require_http_methods(["GET"])
def login(request):
    return render(request, '../templates/login.html', {})

'''
METHOD:GET
URL:/login/loginpermit
RETURN:permit login
ASYNC:false
'''
@csrf_exempt
@require_http_methods(['POST'])
def loginpermit(request):
    username=request.GET.get('username')
    passwd=request.GET.get('passwd')
    #status=service.permitlogin(username,passwd)
    user = authenticate(username=username,password=passwd)
    if user is not None:
        if user.is_active:
            login(request,user)
            return render(request, '../templates/index.html', {})
        else:
            print("aaa")
    else:
        print("bbb")

'''
METHOD:GET
URL:/anweb/index
RETURN:template of page index
ASYNC:true
'''
@require_http_methods(["GET"])
def index(request):
    return render(request, '../templates/index.html', {})

'''
METHOD:GET
URL:/anweb/groupsearch
RETURN:list of group by json
ASYNC:false
'''
@require_http_methods(["GET",])
def groupsearch(request):
    list= service.group9groupsearch()
    return HttpResponse(json.dumps({
        'group_list': list
    }))

'''
METHOD:GET
URL:/anweb/historyget
RETURN: list of history by json
ASYNC:false
'''
@require_http_methods(["GET",])
def historyget(request):
    list= service.historyget()
    return HttpResponse(json.dumps({'history_list':list}))

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
    service.group9modifygroup(group_id, group_name, group_remark)
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
    group_id=request.GET.get('id')
    list= service.host9hostsearch(group_id)
    return HttpResponse(json.dumps({
        'host_list': list
    }))

'''
METHOD:GET
URL:/anweb/hostupdate
POST:ipaddress,group_id
RETURN:null
ASYNC:false
'''
@csrf_exempt
@require_http_methods(["GET"],)
def hostupdate(request):
    ipaddress=request.GET.get('ipaddress')
    group_id=request.GET.get('group')
    status= service.host9hostupdate(ipaddress, group_id);
    return HttpResponse(json.dumps({
        'status': status
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
    list= service.batch9appversion(appname)
    return HttpResponse(json.dumps({
        'host_list': list
    }))


'''
METHOD:POST
URL:/anweb/batchredis
POST:list of redis install info
RETURN:true/false
ASYNC:true
'''
@csrf_exempt
@require_http_methods(["POST"],)
def batchredis(request):#iplist,redisversion,redisprefix,redisport,redispasswd
    iplist = request.POST.getlist('iplist[]')
    version = request.POST.get('version')
    prefix = request.POST.get('prefix')
    port = request.POST.get('port')
    passwd = request.POST.get('passwd')
    datadir = request.POST.get('datadir')
    status = service.batch9redisinstall(iplist, version, prefix, port, passwd, datadir)
    return HttpResponse(json.dumps({
        'status': status
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
    javaprefix=request.POST.get('javaprefix')
    tomcatversion=request.POST.get('tomcatversion')
    tomcatprefix=request.POST.get('tomcatprefix')
    print(iplist,javaversion,javaprefix,tomcatversion,tomcatprefix)
    status= service.batch9tomcatinstall(iplist, javaversion, javaprefix, tomcatversion, tomcatprefix);
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
    version = request.POST.get('version')
    prefix = request.POST.get('prefix')
    passwd=request.POST.get('passwd')
    port=request.POST.get('port')
    datadir=request.POST.get('datadir')
    socket=request.POST.get('socket')
    status= service.batch9mysqlinstall(iplist, version, prefix, passwd, datadir, port, socket, )
    return HttpResponse(json.dumps({
        'status': status
    }))

'''
METHOD:POST
URL:/anweb/batchnginx
POST:list of nginx install info
RETURN:true/false
ASYNC:true
'''
@csrf_exempt
@require_http_methods(["POST"],)
def batchnginx(request):
    iplist = request.POST.getlist('iplist[]')
    version = request.POST.get('version')
    prefix = request.POST.get('prefix')
    pid=request.POST.get('pid');
    status= service.batch9nginxinstall(iplist, version, prefix, pid)
    return HttpResponse(json.dumps({
        'status': status
    }))

'''
METHOD:GET
URL:/anweb/confget
RETURN:
ASYNC:false
'''
@require_http_methods(["GET"],)
def confget(request):
    iplist=request.GET.getlist('iplist[]')
    cnf=request.GET.get('cnf')
    (conf,tmp)= service.cnfget(iplist, cnf)
    return HttpResponse(json.dumps({'conf':conf,'tmp':tmp}))

'''
METHOD:GET
URL:/anweb/confmodify
RETURN:
ASYNC:false
'''
@require_http_methods(["GET"])
def confmodify(request):
    iplist=request.GET.getlist('iplist[]')
    tmp=request.GET.get('tmp')
    newstr=request.GET.get('newstr')
    cnf=request.GET.get('cnf')
    service.cnfmodify(iplist, tmp, newstr, cnf)
    return HttpResponse(json.dumps({'status':1}))

'''
METHOD:GET
URL:/anweb/appget
RETURN:list
ASYNC:false
'''
@require_http_methods(["GET"])
def appget(request):
    appname=request.GET.get('appname')
    list= service.applist(appname)
    return HttpResponse(json.dumps({'applist':list}))

'''
METHOD:GET
URL:/anweb/appcontrol
RETURN:NULL
ASYNC:false
'''
@require_http_methods(["GET"])
def appcontrol(request):
    #{'hostid':hostid,'type':type,'appname':appname};
    hostid=request.GET.get('hostid')
    type=request.GET.get('type')
    appname=request.GET.get('appname')
    service.appcontrol(hostid, type, appname)
    return HttpResponse(json.dumps({'status':'1'}))

'''
METHOD:GET
URL:/anweb/appremove
RETURN:NULL
ASYNC:false
'''
@require_http_methods(['GET'])
def appremove(request):
    hostid=request.GET.get('hostid')
    appname=request.GET.get('appname')
    service.appremove(hostid, appname)
    return HttpResponse(json.dumps({'status':'1'}))