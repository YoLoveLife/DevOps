from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from anweb import service
from django.core.urlresolvers import reverse
import forms
from django.views.generic import View
import json

class LoginView(View):
    def get(self,request):
        login_form=forms.LoginForm()
        return render(request, "login.html", {"login_form": login_form})

    def post(self,request):
        error = ''
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            data=login_form.clean()
            user = authenticate(username=data['email'], password=data['passwd'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                error = 'Error Passwd'
        return render(request, 'login.html', {'error': error, 'login_form': login_form})

class IndexView(View):
    def get(self,request):
        return render(request, "index.html")