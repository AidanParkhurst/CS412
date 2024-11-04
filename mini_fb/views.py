# mini_fb/views.py
# This file contains the views for the mini_fb app.

from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, HttpRequest
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

from .models import Profile, StatusMessage, Image
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm

class ShowAllView(ListView):
    '''A view that shows all the profiles in the database'''

    model = Profile 
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        if current_user.is_authenticated:
            context['current_user'] = Profile.objects.get(user=current_user)
        return context


class ShowProfilePageView(DetailView):
    '''A view that shows a single profile'''

    model = Profile 
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        if current_user.is_authenticated:
            context['current_user'] = Profile.objects.get(user=current_user)
        return context

class CreateProfileView(CreateView):
    '''A view that on GET shows a form to create a new profile'''
    '''And on POST, creates the new profile'''

    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'
    
    def get_success_url(self):
        new_profile = self.object
        return new_profile.get_absolute_url()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
    
        return context
    
    def form_valid(self, form):
        print(self.request.POST)
        user_form = UserCreationForm(self.request.POST)
        user = user_form.save()
        form.instance.user = user
        username = self.request.POST['username']
        password = self.request.POST['password1']
        authenticated = authenticate(username=username, password=password)
        login(self.request, authenticated)
        return super().form_valid(form)
    
    
class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    '''A view that on GET shows a form to create a new status message'''
    '''And on POST, creates the new status message'''

    form_class = CreateStatusMessageForm 
    template_name = 'mini_fb/create_status_form.html'

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['current_user'] = Profile.objects.get(user=self.request.user)
        return context

    def form_valid(self, form):
        form.instance.profile = Profile.objects.get(user=self.request.user)
        sm = form.save()
        files = self.request.FILES.getlist('images')
        # Create a new Image object for each file
        for f in files:
            new_img = Image.objects.create(status_message=sm, image_file=f)
            new_img.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

    def get_login_url(self):
        return reverse('login')

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''A view that on GET shows a form to update an existing profile'''
    '''And on POST, updates the profile'''

    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    model = Profile

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = Profile.objects.get(user=self.request.user)
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})

    def get_login_url(self):
        return reverse('login')

class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    '''A view that on GET shows a form to update an existing status message'''
    '''And on POST, updates the status message'''

    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'
    model = StatusMessage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = StatusMessage.objects.get(pk=self.kwargs['pk'])
        context['current_user'] = Profile.objects.get(user=self.request.user)
        return context

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

    def get_login_url(self):
        return reverse('login')

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    '''A view that on GET shows a form to delete an existing status message'''
    '''And on POST, deletes the status message'''

    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = StatusMessage.objects.get(pk=self.kwargs['pk'])
        context['current_user'] = Profile.objects.get(user=self.request.user)
        context['profile'] = status.profile
        return context

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
    def get_login_url(self):
        return reverse('login')
    
class CreateFriendView(LoginRequiredMixin, View):
    '''A view that creates a friendship between two profiles'''

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        friend = Profile.objects.get(pk=self.kwargs['other_pk'])
        profile.add_friend(friend)

        return redirect(reverse('show_profile', kwargs={'pk': profile.pk}))
    
    def get_login_url(self):
        return reverse('login')
    
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    '''A view that shows friend suggestions for a profile'''

    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['current_user'] = Profile.objects.get(user=self.request.user)
        context['suggested_friends'] = profile.get_friend_suggestions()
        return context
    
    def get_login_url(self):
        return reverse('login')
    
class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    '''A view that shows the news feed for a profile'''

    model = Profile 
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['news_feed'] = profile.get_news_feed()
        context['current_user'] = profile
        return context
    
    def get_login_url(self):
        return reverse('login')
    