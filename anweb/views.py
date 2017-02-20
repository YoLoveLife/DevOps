from django.shortcuts import render
# Create your views here.
from event import allevent
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET","POST"])
def index(request):
    #return HttpResponse('this is test result')
    return render(request, 'index.html',{})


@require_http_methods(["GET","POST"])
def Index(request):
    #servicer_list=Servicer.objects.all().order_by('id')
    return render(request, 'index.html',{
                                   #      'servicer':encoder.toJSON(servicer_list[0]),
                                         })