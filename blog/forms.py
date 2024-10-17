from django import forms
from .models import Article, Comment

class CreateCommentForm(forms.ModelForm):
    '''A form to add a Comment to the database.'''
    class Meta:
        '''associate this form with the Comment model; select fields.'''
        model = Comment
        fields = ['author', 'text', ]  # which fields from model should we use

class CreateArticleForm(forms.ModelForm):
    '''A form to add an Article to the database.'''
    author = forms.CharField(max_length=100, required=True)
    class Meta:
        '''associate this form with the Article model; select fields.'''
        model = Article
        fields = ['title', 'author', 'text', 'img_file']  # which fields from model should we use