from django.contrib.auth import authenticate,login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from models import Group

class ManagerGroupView(View):
    def get(self,request):
        grouplist = Group.objects.all()
        return render(request, 'group.html', {'grouplist': grouplist})