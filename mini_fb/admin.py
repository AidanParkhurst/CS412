# mini_fb/admin.py
# This file is used to register the models with the Django admin interface.
from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)
admin.site.register(Friend)