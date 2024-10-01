# blog/views.py
# This file contains the views for the blog app.

from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.views.generic import ListView

from .models import Article

class ShowAllView(ListView):
    '''A view that shows all the articles in the database'''

    model = Article
    template_name = 'blog/home.html'
    context_object_name = 'posts'