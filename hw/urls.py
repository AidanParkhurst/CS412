## hw/urls.py
## description: URL patterns for the hw app

from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path(r'', views.home, name='home'),
]