from django.shortcuts import render
# Create your views here.
from event import allevent
from django.http import HttpResponse
from django.views.generic.detail import DetailView
def index(request):
    #return HttpResponse('this is test result')
    return render(request, 'index.html')