## hw/views.py
## description: handles url requests for the hw app

from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

import time
import random

# Create your views here.
def home(request: HttpRequest):
    '''Returns a simple response to the request'''

    template_name = 'hw/home.html'

    context = {
        'time': time.ctime(),
        'random_number': random.randint(1, 100),
    }

    return render(request, template_name, context) 