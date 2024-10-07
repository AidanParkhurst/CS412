# mini_fb/views.py
# This file contains the views for the mini_fb app.

from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.views.generic import ListView

from .models import Profile 

class ShowAllView(ListView):
    '''A view that shows all the profiles in the database'''

    model = Profile 
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'