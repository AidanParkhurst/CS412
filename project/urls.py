## project/urls.py
## description: URL patterns for my final project 

from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path(r'', views.Home.as_view(), name='home'),
    path(r'all_clubs/', views.AllClubs.as_view(), name='all_clubs'),
    path(r'club/<int:pk>/', views.ClubDetail.as_view(), name='view_club'),
    path(r'club/<int:pk>/edit/', views.EditClub.as_view(), name='edit_club'),
    path(r'club/<int:pk>/delete_competitor/', views.DeleteCompetitor.as_view(), name='delete_competitor'),
    path(r'club/<int:pk>/update_competitor/', views.UpdateCompetitor.as_view(), name='update_competitor'),
    path(r'club/<int:pk>/add_competitor/', views.AddCompetitor.as_view(), name='add_competitor'),
    path(r'competition/<int:pk>/', views.CompetitionDetail.as_view(), name='view_competition'),
    path(r'competition/<int:pk>/bracket', views.BracketView.as_view(), name='view_bracket'),
    path(r'competition/<int:pk>/bracket/generate', views.GenerateBracket.as_view(), name='generate_bracket'),
    path(r'competition/<int:pk>/bracket/set_winner/', views.SetWinner.as_view(), name='set_winner'),
    path(r'competition/<int:pk>/register/', views.JoinCompetition.as_view(), name='join_competition'),
    path(r'competition/<int:pk>/unregister/', views.LeaveCompetition.as_view(), name='leave_competition'),
    path(r'create_competition/', views.CreateCompetition.as_view(), name='create_competition'),
    path(r'signup/', views.SignUp.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]