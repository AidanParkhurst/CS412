# blog/models.py
# Define the data structures for the blog app

from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now_add=True)
    # img = models.URLField(blank=True)
    img_file = models.ImageField(blank=True)

    def __str__(self):
        return self.title + " by " + self.author

    def get_comments(self):
        '''Return all of the comments about this article.'''
        comments = Comment.objects.filter(article=self)
        return comments
    
    def get_absolute_url(self):
        '''Return the URL to display this article.'''
        return reverse('article', kwargs={'pk': self.pk})

class Comment(models.Model):
    '''Encapsulate the idea of a Comment on an Article.'''
    
    # data attributes of a Comment:
    article = models.ForeignKey("Article", on_delete=models.CASCADE)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        '''Return a string representation of this Comment object.'''
        return f'{self.text}'