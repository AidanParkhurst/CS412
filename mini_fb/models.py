# mini_fb/models.py
# Define the data structures for the mini_fb app

from django.shortcuts import reverse
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

    # Return all the status messages for this profile, ordered by timestamp
    def get_status_messages(self):
        '''Return all of the status messages for this profile.'''
        messages = StatusMessage.objects.filter(profile=self).order_by('timestamp')
        return messages
    
    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk})
    
class StatusMessage(models.Model):
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
    
    def get_images(self):
        '''Return all of the images for this status message.'''
        images = Image.objects.filter(status_message=self)
        return images

class Image(models.Model):
    status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)
    image_file = models.ImageField()
    timestamp = models.DateTimeField(auto_now_add=True)