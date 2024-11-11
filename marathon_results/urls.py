## marathon_results/urls.py
## description: URL patterns for the marathon_results app

from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path(r'', views.ResultsListView.as_view(), name='home'),
    path(r'results/', views.ResultsListView.as_view(), name='results_list'),
]