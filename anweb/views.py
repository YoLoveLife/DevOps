from django.shortcuts import render

# Create your views here.
from event import allevent
from django.http import HttpResponse

def test(request):
    allevent.evt_shell_control('redis-server',control='echo "This is test">>/test.txt')
    return HttpResponse('this is test result')
