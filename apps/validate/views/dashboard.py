from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class ValidateDashBoardView(LoginRequiredMixin,TemplateView):
    template_name = 'ddashboard.html'
    def get_context_data(self, **kwargs):
        context=super(ValidateDashBoardView,self).get_context_data(**kwargs)
        context.update({
        })
        return context

    def get(self,request,*args,**kwargs):
        return super(ValidateDashBoardView,self).get(request,*args,**kwargs)