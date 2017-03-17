from django.shortcuts import render
# Create your views here.
from event import allevent
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from anweb.models import Group,Host
from django.core import serializers
from util import toJSON
from anweb import model2json
import json
'''
METHOD:GET
URL:/anweb
RETURN:template of page index
ASYNC:true
'''
@require_http_methods(["GET"])
def index(request):
    #return HttpResponse('this is test result')
    return render(request, 'index.html',{})

'''
METHOD:GET
URL:/anweb/groupsearch
RETURN:list of group by json
ASYNC:false
'''
@require_http_methods(["GET",])
def groupsearch(request):
    a = Group.objects.all()
    list = []
    for i in a:
        list.append(toJSON(i))
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
    group_id=request.POST.get('groupid');
    group_name=request.POST.get('groupname');
    group_remark=request.POST.get('groupremark');
    if group_id == "0":#ADD
        group=Group(group_name=unicode.encode(group_name),remark=unicode.encode(group_remark))
        group.save()
        return HttpResponse(json.dumps({
            'status': "add"
        }))
    else:#UPDATE
        Group.objects.filter(id=int(group_id)).update(group_name=unicode.encode(group_name),remark=unicode.encode(group_remark))
        return HttpResponse(json.dumps({
            'status': "update"
        }))

'''
METHOD:POST
URL:/anweb/hostsearch
POST:groupid
RETURN:list of host for groupid
ASYNC:false
'''
@csrf_exempt
@require_http_methods(["POST"],)
def hostsearch(request):
    group_id=request.POST.get('group_id');
    a=Host.objects.filter(group_id=int(group_id))
    list = []
    '''
    for i in a:
        list.append(toJSON(i))
        print(type(i))
    '''
    data=serializers.serialize('json',a,)
    model2json.host9hostsearch(data)
    return HttpResponse(json.dumps({
        'host_list': list
    }))
