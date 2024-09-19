## quotes/views.py
## description: handles url requests for the hw app

from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

import time
import random

quotes = [
    "I don't defeat my opponents, they defeat themselves.",
    "Usually, a well thought answer makes an aggressor think twice.",
    "For a choke, there are no tough guys.",
    "Always assume that your opponent is going to be bigger, stronger, and faster than you; so that you learn to rely on technique, timing, and leverage rather than brute strength.",
]

images = [
    "https://scarsdaleaikido.com/img/helio-gracie-jiu-jitsu-vale-tudo.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/H%C3%A9lio_Gracie_%281952%29.tif/lossy-page1-220px-H%C3%A9lio_Gracie_%281952%29.tif.jpg",
    "https://cdn.shopify.com/s/files/1/0030/3742/9849/files/2_d45434b8-4f77-44e5-877c-9dfc1a45d5c1.jpg?v=1650307527",
    "https://i.redd.it/hwb7qmu7rbq21.png",
]

# Create your views here.
def quote(request: HttpRequest):
    '''Returns a simple response to the request'''

    template_name = 'quotes/quote.html'

    context = {
        'random_quote': random.choice(quotes),
        'random_image': random.choice(images),
    }

    return render(request, template_name, context) 


def about(request: HttpRequest):
    '''Returns a simple response to the request'''

    template_name = 'quotes/about.html'

    context = {
    }

    return render(request, template_name, context) 

def show_all(request: HttpRequest):
    '''Returns a simple response to the request'''

    template_name = 'quotes/show_all.html'

    context = {
        'quotes': quotes,
        'image0': images[0],
        'image1': images[1],
        'image2': images[2],
        'image3': images[3],
    }

    return render(request, template_name, context)