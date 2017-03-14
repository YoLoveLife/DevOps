from django.shortcuts import render
# Create your views here.
from event import allevent
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from anweb.models import Group
from django.forms.models import model_to_dict
from django.core import serializers
from util import toJSON
import json
@require_http_methods(["GET","POST"])
def index(request):
    #return HttpResponse('this is test result')
    return render(request, 'index.html',{})

@require_http_methods(["GET",])
def groupsearch(request):
    a = Group.objects.all()
    list = []
    for i in a:
        list.append(toJSON(i))

    return HttpResponse(json.dumps({
        'group_list': list
    }))

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
        Group.objects.filter(group_name=unicode.encode(group_name),remark=unicode.encode(group_remark));
        return HttpResponse(json.dumps({
            'status': "update"
        }))


'''
@require_http_methods(["GET",])
def get_group_list(request,position):
    print(position)
    if position == '0':
        a = Group.objects.all()
    else:
        a=Group.objects.get(id=int(position))
    list = []
    for i in a:
        list.append(toJSON(i))
    return HttpResponse(json.dumps({
        'group_list': list
    }))

@require_http_methods(["GET","POST"])
def Index(request):
    #servicer_list=Servicer.objects.all().order_by('id')
    return render(request, 'index.html',{
                                   #      'servicer':encoder.toJSON(servicer_list[0]),
                                         })

@require_http_methods(["GET",])
def get_group_list(request):
    group_list=Group.objects.all()
    list={}
    for group in group_list:
        list=list+toJSON(group)
    print(list)
    return HttpResponse(json.dumps({
            'group_list':json.dumps(serializers.serialize("json",Group.objects.all())),
        }))
'''