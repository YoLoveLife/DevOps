# -*- coding:utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from .. import forms,models
from timeline.models import History
from manager.models import Group
from ..permission import script as ScriptPermission
from ..permission import playbook as PlaybookPermission
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.detail import DetailView
from .. import MODULE_OPTION
from timeline.decorator.manager import decorator_manager

class OperationPlaybookListView(LoginRequiredMixin,TemplateView):
    template_name= 'operation/playbook.html'

    def get_context_data(self, **kwargs):
        context= super(OperationPlaybookListView, self).get_context_data(**kwargs)
        return context

    def get(self,request,*args, **kwargs):
        return super(OperationPlaybookListView, self).get(request, *args, **kwargs)

class OperationPlaybookUpdateView(LoginRequiredMixin,PlaybookPermission.PlaybookAddRequiredMixin,PlaybookPermission.PlaybookChangeRequiredMixin,UpdateView):
    template_name = 'operation/new_update_playbook.html'
    form_class = forms.PlaybookCreateUpdateForm
    success_url = reverse_lazy('operation:playbook')
    model = models.PlayBook
    id = 0

    def get_object(self, queryset=None):
        if self.kwargs['pk'] == '0':
            user = self.request.user
            if models.PlayBook.objects.filter(author=user,status=0).exists(): #查询未完成脚本
                playbook=models.PlayBook.objects.filter(author=user,status=0)[0]
            else:
                playbook=models.PlayBook.objects.create()
            self.id=playbook.id
            return playbook
        else:
            self.id=self.kwargs['pk']
            return models.PlayBook.objects.get(id = self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(OperationPlaybookUpdateView,self).get_context_data(**kwargs)
        grouplist = models.Group.objects.all()
        playbook_groups=[group.id for group in self.object.groups.all()]

        context.update({
            'id':self.id,
            'grouplist':grouplist,
            'playbook_groups':playbook_groups,
        })
        return context

    @decorator_manager(2,u'剧本编辑')
    def form_valid(self, form):
        playbook_info=form.save()
        groups_id_list = self.request.POST.getlist('groups',[])
        groups = models.Group.objects.filter(id__in=groups_id_list)
        playbook_info.groups.clear()
        playbook_info.groups.add(*groups)

        # status=self.request.POST.get('status')
        # if status == '0':
        #     playbook_info.status = 0
        # else:
        #     playbook_info.status = 1
        playbook_info.save()

        return self.request.user,super(OperationPlaybookUpdateView, self).form_valid(form)

    def get_success_url(self):
        return self.success_url

class OperationTaskEditorView(LoginRequiredMixin,TemplateView):
    template_dir = 'operation/module/'
    postfix = '.html'

    def get_context_data(self, **kwargs):
        context= super(OperationTaskEditorView, self).get_context_data(**kwargs)
        module = self.kwargs['pk']
        if self.kwargs.has_key('pkp'):
            scripts = models.Script.objects.filter(author_id__exact=self.request.user.id)
            context.update({
                'scripts' : scripts
            })
        self.template_name = self.template_dir + MODULE_OPTION[module]+self.postfix
        return context

    def get(self,request,*args, **kwargs):
        return super(OperationTaskEditorView, self).get(request, *args, **kwargs)