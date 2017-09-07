from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .. import forms

class ValidateUserListView(LoginRequiredMixin,TemplateView):
    template_name='validate/user.html'
    #form_class = forms.UserForm

    def get_context_data(self, **kwargs):
        context= super(ValidateUserListView, self).get_context_data(**kwargs)
        # context.update({'grouplist': models.Group.objects.all(),
        #                 })
        return context

    def get(self,request,*args, **kwargs):
        return super(ValidateUserListView, self).get(request, *args, **kwargs)