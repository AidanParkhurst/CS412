## blog/urls.py
## description: URL patterns for the blog app

from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path(r'', views.ShowAllView.as_view(), name='blog_home'),
    path(r'article/<int:pk>', views.ArticleDetailView.as_view(), name='article'),
    path(r'random', views.RandomArticleView.as_view(), name='random'),
    path(r'article/<int:pk>/create_comment', views.CreateCommentView.as_view(), name='create_comment'),
    path(r'create_article', views.CreateArticleView.as_view(), name='create_article'),
]