from django.shortcuts import render
# Create your views here.
from event import allevent
from django.http import HttpResponse

def test(request):
    #return HttpResponse('this is test result')
    return render(request, 'index.html')
