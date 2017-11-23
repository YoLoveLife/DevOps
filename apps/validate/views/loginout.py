# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import FormView
from django.views.generic import View
from .. import forms
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

class ValidateLoginView(FormView):
    template_name = 'validate/login.html'
    form_class= forms.LoginForm
    redirect_field_name='yo'

    def get(self,request, *args, **kwargs):
        return super(ValidateLoginView,self).get(request,*args,**kwargs)

    def post(self,request,*args, **kwargs):
        error=u'none'
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            data=login_form.clean()

            if data['verify'] != request.session.get('verifycode'):
                error = u'错误的验证码'
                return render(request, self.template_name, {'error': error, 'form': login_form})

            user = authenticate(username=data['username'], password=data['passwd'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                error = u'错误的账户或者密码'
                return render(request, self.template_name, {'error': error, 'form': login_form})
        return render(request,self.template_name, {'error': error, 'form': login_form})

class ValidateCodeView(View):
    def verifycode_maker(self,request):
        import random
        from PIL import Image,ImageDraw,ImageFont
        import cStringIO
        bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 255)
        width = 100
        height = 25
        im = Image.new('RGB', (width, height), bgcolor)
        draw = ImageDraw.Draw(im)
        for i in range(0, 100):
            xy = (random.randrange(0, width), random.randrange(0, height))
            fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
            draw.point(xy, fill=fill)
        str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
        rand_str = ''
        for i in range(0, 4):
            rand_str += str1[random.randrange(0, len(str1))]
        font = ImageFont.truetype('validate/fonts/FreeMono.ttf', 23)
        fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
        draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
        draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
        draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
        draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
        del draw
        request.session['verifycode'] = rand_str
        buf = cStringIO.StringIO()
        im.save(buf, 'png')
        return buf

    def get(self,request,*args,**kwargs):
        buf =self.verifycode_maker(request=request)
        return HttpResponse(buf.getvalue(),'image/png')


class ValidateLogoutView(LoginRequiredMixin,View):
    template_name='validate/login.html'
    form_class= forms.LoginForm
    def get(self,request):
        logout(request)
        return HttpResponseRedirect('/')

