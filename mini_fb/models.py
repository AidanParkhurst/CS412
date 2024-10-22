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
    
    def get_friends(self):
        '''Return all of the friends for this profile.'''
        friends = Friend.objects.filter(profile1=self) | Friend.objects.filter(profile2=self)
        profiles = []
        for friend in friends:
            if friend.profile1 == self:
                profiles.append(friend.profile2)
            else:
                profiles.append(friend.profile1)

        return profiles
    
    def add_friend(self, friend):
        if self == friend:
            return

        friends = Friend.objects.filter(profile1=self) | Friend.objects.filter(profile2=self)
        for f in friends:
            if (f.profile1 == friend or f.profile2 == friend):
                return

        new_friend = Friend(profile1=self, profile2=friend)
        new_friend.save()

    def get_friend_suggestions(self):
        '''Return a list of profiles that are friends of friends of this profile, but not this profile's friends.'''
        friends = self.get_friends()
        suggestions = []
        for friend in friends:
            friend_friends = friend.get_friends()
            for f in friend_friends:
                if f not in suggestions and f not in friends and f != self:
                    suggestions.append(f)

        if len(suggestions) == 0:
            # If no friends of friends are found, return random profiles that are not this, and not friends of this
            all_profiles = Profile.objects.all()
            for profile in all_profiles:
                if profile != self and profile not in friends:
                    suggestions.append(profile)
                    if len(suggestions) == 3:
                        break

        return suggestions

    def get_news_feed(self):
        '''Return a list of status messages for this profile and all of its friends, ordered by timestamp.'''
        friends = self.get_friends()
        friends.append(self)
        messages = StatusMessage.objects.filter(profile__in=friends).order_by('timestamp')
        return messages 

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

class Friend(models.Model):
    profile1 = models.ForeignKey("Profile", related_name="profile1", on_delete=models.CASCADE)
    profile2 = models.ForeignKey("Profile", related_name="profile2", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.profile1.first_name + " " + self.profile1.last_name + " & " + self.profile2.first_name + " " + self.profile2.last_name
