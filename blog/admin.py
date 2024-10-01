# blog/admin.py
# This file is used to register the models with the Django admin interface.
from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Article)