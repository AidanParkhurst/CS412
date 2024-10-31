## blog/urls.py
## description: URL patterns for the blog app

from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path(r'', views.ShowAllView.as_view(), name='blog_home'),
    path(r'article/<int:pk>', views.ArticleDetailView.as_view(), name='article'),
    path(r'random', views.RandomArticleView.as_view(), name='random'),
    path(r'article/<int:pk>/create_comment', views.CreateCommentView.as_view(), name='create_comment'),
    path(r'create_article', views.CreateArticleView.as_view(), name='create_article'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='blog_home'), name='logout'),
    path('register/', views.RegistrationView.as_view(), name='register'),
]