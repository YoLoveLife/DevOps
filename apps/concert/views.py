# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from permission import music as MusicPermisson
from django.views.generic import TemplateView
from django.urls import reverse_lazy
# Create your views here.

class ConcertMusicListView(LoginRequiredMixin,TemplateView):
    template_name='concert/music.html'

    def get_context_data(self, **kwargs):
        context= super(ConcertMusicListView, self).get_context_data(**kwargs)
        return context

    def get(self,request,*args, **kwargs):
        return super(ConcertMusicListView, self).get(request, *args, **kwargs)