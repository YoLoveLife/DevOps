# -*- coding:utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from .. import forms,models
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.detail import DetailView

class OperationScriptListView(LoginRequiredMixin,TemplateView):
    template_name= 'operation/script.html'
    form_class = forms.ScriptForm

    def get_context_data(self, **kwargs):
        context= super(OperationScriptListView, self).get_context_data(**kwargs)
        return context

    def get(self,request,*args, **kwargs):
        return super(OperationScriptListView, self).get(request, *args, **kwargs)


class OperationScriptUpdateView(LoginRequiredMixin,UpdateView):
    template_name = 'operation/new_update_script.html'
    form_class = forms.ScriptCreateUpdateForm
    success_url = reverse_lazy('operation:script')
    model = models.Script
    id = 0
    def get_object(self, queryset=None):
        if self.kwargs['pk'] == '0':
            user = self.request.user
            if models.Script.objects.filter(author=user,status=0).exists(): #查询未完成脚本
                script=models.Script.objects.filter(author=user,status=0)[0]
            else:
                script=models.Script.objects.create()
            self.id=script.id
            return script
        else:
            self.id=self.kwargs['pk']
            return models.Script.objects.get(id = self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(OperationScriptUpdateView,self).get_context_data(**kwargs)

        context.update({
            'id':self.id
        })
        return context
    
    def form_valid(self, form):
        script_info=form.save()
        status=self.request.POST.get('status')
        if status == '0':
            script_info.status = 0
        else:
            script_info.status = 1
        script_info.save()
        return super(OperationScriptUpdateView, self).form_valid(form)

    def get_success_url(self):
        return self.success_url


class OperationScriptDetailView(LoginRequiredMixin,DetailView):
    model = models.Script
    template_name = 'operation/detail_script.html'

    def get_context_data(self, **kwargs):
        context=super(OperationScriptDetailView,self).get_context_data(**kwargs)
        script=self.object
        context.update({
            'script':script
        })
        return context