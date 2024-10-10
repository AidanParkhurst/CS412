# blog/views.py
# This file contains the views for the blog app.

from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpRequest
from django.views.generic import ListView, DetailView, CreateView

from .models import Article
from .forms import CreateCommentForm
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