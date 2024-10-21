# mini_fb/forms.py
# This file describes how this apps models should be presented in forms. 

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    '''A form to create a new profile'''
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    city = forms.CharField(label='City', max_length=100)
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'profile_picture_url']

class UpdateProfileForm(forms.ModelForm):
    '''A form to update an existing profile'''
    class Meta:
        model = Profile
        fields = ['city', 'email', 'profile_picture_url']

class CreateStatusMessageForm(forms.ModelForm):
    '''A form to create a new status message'''
    class Meta:
        model = StatusMessage
        fields = ['message']