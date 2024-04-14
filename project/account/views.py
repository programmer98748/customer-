from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import FormView, View
from .forms import UserLoginForm
 #UserProfileForm

class LoginPage(LoginView):
    template_name = 'account/login.html'
    form_class = UserLoginForm
    
    def get(self, request, *args, **kwargs):
     
        if request.user.is_authenticated:
            if '?next=/' in request.get_full_path():
                return super().get(request, *args, **kwargs)
            else:
                return redirect('dashbaord:home')


        return super().get(request, *args, **kwargs)
 

 
    