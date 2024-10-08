## blog/urls.py
## description: URL patterns for the blog app

from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path(r'', views.ShowAllView.as_view(), name='blog_home'),
]