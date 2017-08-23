from django.shortcuts import render
from django.views.generic import FormView
from django.views.generic import View
from ..forms import LoginForm
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect