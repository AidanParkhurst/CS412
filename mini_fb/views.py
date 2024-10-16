# mini_fb/views.py
# This file contains the views for the mini_fb app.

from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpRequest
from django.views.generic import ListView, DetailView, CreateView

from .models import Profile, StatusMessage
from .forms import CreateProfileForm, CreateStatusMessageForm

class ShowAllView(ListView):
    '''A view that shows all the profiles in the database'''

    model = Profile 
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    '''A view that shows a single profile'''

    model = Profile 
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CreateProfileView(CreateView):
    '''A view that on GET shows a form to create a new profile'''
    '''And on POST, creates the new profile'''

    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'
    
    def get_success_url(self):
        new_profile = self.object
        return new_profile.get_absolute_url()
    
class CreateStatusMessageView(CreateView):
    '''A view that on GET shows a form to create a new status message'''
    '''And on POST, creates the new status message'''

    form_class = CreateStatusMessageForm 
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.profile = Profile.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})

