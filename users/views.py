from django.urls.base import reverse_lazy
from plasma_link.models import Donor
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DeleteAccountForm, UserRegisterForm
from django.contrib.auth import login
from django.conf import settings
import urllib
import json
from g_recaptcha.validate_recaptcha import validate_captcha
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

@validate_captcha
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
                user = form.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, f'Account created for {user.username}. Make sure you remember your username and password!')
                return redirect('donor_registration')  
    else:
        form = UserRegisterForm() 
    context = {'form': form}
    
    context['GOOGLE_RECAPTCHA_SITE_KEY'] = settings.GOOGLE_RECAPTCHA_SITE_KEY
    return (render(request, 'users/register.html', context))   

def delete_account(request):
    context = {}
    user = request.user
    context['user'] = user

    if request.method == 'POST':
        form = DeleteAccountForm(request.POST)
        if form.is_valid():
            user.delete()
            messages.success(request, f'Account deleted for {user.username}.')
            return reverse_lazy('find_donor') 
    else:
        form = DeleteAccountForm() 
    context['form'] = form
    
    return (render(request, 'users/delete_account.html', context))


