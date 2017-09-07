from django.contrib.auth import authenticate,login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from apps.validate import forms


class LoginView(View):
    def get(self,request):
        login_form= forms.LoginForm()
        return render(request, "../templates/validate/login.html", {"login_form": login_form})

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
        return render(request, '../templates/validate/login.html', {'error': error, 'login_form': login_form})

class IndexView(View):
    def get(self,request):
        return render(request, "../templates/index.html")