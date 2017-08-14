from django.contrib.auth.mixins import LoginRequiredMixin
from .. import forms
from .. import models
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.detail import DetailView

class OperationScriptListView(LoginRequiredMixin,TemplateView):
    template_name='script.html'
    form_class = forms.ScriptForm

    def get_context_data(self, **kwargs):
        context= super(OperationScriptListView, self).get_context_data(**kwargs)
        return context

    def get(self,request,*args, **kwargs):
        return super(OperationScriptListView, self).get(request, *args, **kwargs)


class OperationScriptCreateView(LoginRequiredMixin,CreateView):
    model = models.Script
    form_class = forms.ScriptCreateUpdateForm
    template_name = 'new_update_script.html'
    success_url = reverse_lazy('operation:script')

    def form_valid(self, form):
        script_form=form.save()
        script_form.save()
        return super(OperationScriptCreateView,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(OperationScriptCreateView,self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return self.success_url