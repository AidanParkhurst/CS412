# project/forms.py
# This file describes how this apps models should be presented in forms. 

from django import forms
from .models import Club, Competition, Competitor

class ClubCreationForm(forms.ModelForm):
    '''A form to create a new club'''
    class Meta:
        model = Club
        fields = ['NAME']
        labels = {
            'NAME': 'Club Name',
        }

class CompCreationForm(forms.ModelForm):
    '''A form to create a new competition'''
    class Meta:
        model = Competition
        fields = ['LOCATION', 'DATE', 'MAT_COUNT', 'MATCHES_PER_COMPETITOR']
        widgets = {
            'DATE': forms.DateInput(attrs={'type': 'date'}),
        }
