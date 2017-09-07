from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class ValidateDashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'validate/dashboard.html'
    def get_context_data(self, **kwargs):
        context=super(ValidateDashboardView,self).get_context_data(**kwargs)
        context.update({
        })
        return context

    def get(self,request,*args,**kwargs):
        return super(ValidateDashboardView,self).get(request,*args,**kwargs)