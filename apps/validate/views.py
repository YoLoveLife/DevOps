from django.shortcuts import redirect,render
from django.views.generic import TemplateView
from django.views.generic import View
from .forms import LoginForm
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
class LoginView(TemplateView):
    template_name= 'login.html'
    form_class= LoginForm
    redirect_field_name='next'

    def get(self,request, *args, **kwargs):
        login_form= LoginForm()
        #return super(LoginView, self).get(request, *args, **kwargs)
        return render(request,self.template_name, {'login_form': login_form})

    def post(self,request):
        error = ''
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            data=login_form.clean()
            user = authenticate(username=data['email'], password=data['passwd'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                error = 'Error Passwd'
        return render(request,self.template_name, {'error': error, 'login_form': login_form})

class LogoutView(View):
    template_name='login.html'
    def get(self,request):
        logout(request)
        return render(request,self.template_name,{'msg':'logout success'})