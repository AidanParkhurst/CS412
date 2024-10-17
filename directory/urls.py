## directory/urls.py
## description: URL patterns for the directory app

from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path(r'', views.home, name='directory_home'),
]
