# blog/views.py
# This file contains the views for the blog app.

from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, HttpRequest
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User 
from django.contrib.auth import login 

from .models import Article
from .forms import CreateArticleForm, CreateCommentForm
import random

class ShowAllView(ListView):
    '''A view that shows all the articles in the database'''

    model = Article
    template_name = 'blog/home.html'
    context_object_name = 'posts'

class RandomArticleView(DetailView):
    '''A view that shows a random article'''

    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'post'

    def get_object(self):
        '''Return a random article'''
        articles = Article.objects.all()
        return random.choice(articles)

class ArticleDetailView(DetailView):
    '''A view that shows a single article'''

    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'post'

class CreateCommentView(CreateView):
    form_class = CreateCommentForm
    template_name = 'blog/create_comment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = Article.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.article = Article.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('article', kwargs={'pk': self.kwargs['pk']})
    
class CreateArticleView(LoginRequiredMixin, CreateView):
    '''A view that allows a user to create a new article'''

    form_class = CreateArticleForm
    template_name = 'blog/create_article.html'

    def get_login_url(self):
        return reverse('login')

    def form_valid(self, form):
        print(form.cleaned_data)
        form.instance.user = self.request.user
        return super().form_valid(form)

class RegistrationView(CreateView):

    template_name = 'blog/register.html'
    form_class = UserCreationForm

    def dispatch(self, *args, **kwargs):
        '''
        Handle the User creation part of the form submission, 
        '''
        # handle the POST:
        if self.request.POST:
            # reconstruct the UserCreationForm from the POST data
            user_form = UserCreationForm(self.request.POST)

            if not user_form.is_valid():
                return super().dispatch(self.request, *args, **kwargs)
            # create the user and login
            user = user_form.save()     
            print(f"RegistrationView.form_valid(): Created user= {user}")

            login(self.request, user)
            print(f"RegistrationView.form_valid(): User is logged in")   
            
            # for mini_fb: attach the user to the Profile instance object so that it 
            # can be saved to the database in super().form_valid()
            return redirect(reverse('blog_home'))
        
        # GET: handled by super class
        return super().dispatch(self.request, *args, **kwargs)
        