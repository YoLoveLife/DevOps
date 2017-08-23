from django.shortcuts import render
from django.views.generic import FormView
from django.views.generic import View
from ..forms import LoginForm
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
class ValidateLoginView(FormView):
    template_name= 'login.html'
    form_class= LoginForm
    redirect_field_name='yo'

    def get(self,request, *args, **kwargs):
        return super(ValidateLoginView,self).get(request,*args,**kwargs)

    def post(self,request,*args, **kwargs):
        error = 'nowhere'
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            data=login_form.clean()
            user = authenticate(username=data['username'], password=data['passwd'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                error = 'Error Passwd'
        return render(request,self.template_name, {'error': error, 'form': login_form})


class ValidateLogoutView(View):
    template_name='login.html'
    form_class= LoginForm
    def get(self,request):
        logout(request)
        return HttpResponseRedirect('/')