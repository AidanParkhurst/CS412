# mini_fb/models.py
# Define the data structures for the mini_fb app

from django.db import models

# Create your models here.

class Profile(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    city = models.TextField()
    email = models.TextField()
    profile_picture_url = models.URLField()

    def __str__(self):
        return self.first_name + " " + self.last_name