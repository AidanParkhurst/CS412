## voter_analytics/urls.py
## description: URL patterns for the voter_analytics app

from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>/', views.VoterDetailView.as_view(), name='voter'),
    path('graphs/', views.VoterStatsView.as_view(), name='graphs'),
]