from django.contrib.auth import authenticate,login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from models import Group
from forms import GroupForm

class ManagerGroupListView(LoginRequiredMixin,FormView):
    template_name= 'group.html'
    form_class=GroupForm

    def get_context_data(self, **kwargs):
        context= super(ManagerGroupListView, self).get_context_data(**kwargs)
        grouplist = Group.objects.all()
        group_form=GroupForm()
        context.update({'grouplist': grouplist,
                        })
        return context

    def get(self,request,*args, **kwargs):
        return super(ManagerGroupListView, self).get(request, *args, **kwargs)

    def post(self,request,*args, **kwargs):
        error=""
        group_form = GroupForm(request.POST)
        if group_form.is_valid():
            data=group_form.clean()
        return render(request,self.template_name,{'error':error,'form':group_form})


class ManagerHostListView(LoginRequiredMixin,TemplateView):
    template_name='host.html'
    #form_class=

    def get(self,request):
        grouplist = Group.objects.all()
        return render(request,self.template_name,{'grouplist':grouplist})

    def post(self,request):
        return
