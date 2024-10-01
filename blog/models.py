# blog/models.py
# Define the data structures for the blog app

from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=100)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now_add=True)
    img = models.URLField(blank=True)

    def __str__(self):
        return self.title + " by " + self.author