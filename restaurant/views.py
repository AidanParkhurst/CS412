# restaurant/views.py
# Handles requests and responses for the restaurant app

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
import random
import time

specials = [
    "The Serious Swiss",
    "The Turkeynator",
    "The Beefy Boy",
    "Veggie Delight",
    "The Chicken Supreme",
]

items = {
    "bgc": ['Bacon Pickled Onion Grilled Cheese', 6.99],
    "tec": ['Taylor Ham Egg & Cheese on a Bagel', 7.99],
    "prp": ['Proscuitto & Roasted Peppers in Balsamic', 8.99],
    "cof": ['Hot Coffee', 1.99],
    "milk": ['Milk', 0.50],
    "sugar": ['Sugar', 0.25],
}

def main(request: HttpRequest):
    '''Returns a simple response to the request'''

    template_name = 'restaurant/main.html'

    return render(request, template_name)

def order(request: HttpRequest):
    '''Displays the menu'''

    template_name = 'restaurant/order.html'

    special = random.choice(specials)
    context = {
        'special': special,
    }
    return render(request, template_name, context)

def confirmation(request: HttpRequest):
    '''Handles form submission'''

    if request.POST:
        template_name = 'restaurant/confirmation.html'

        total_cost = 0
        items_ordered = []
        for item in items:
            if request.POST.get(item):
                total_cost += items[item][1]
                items_ordered.append(items[item][0])

        if request.POST.get('spc'):
            total_cost += 9.99
            items_ordered.append(request.POST.get('special'))

        prep_time = random.randint(30, 60)
        ready_time = time.strftime('%I:%M %p', time.localtime(time.time() + prep_time * 60))
        context = {
            'order_items': items_ordered,
            'total_cost': total_cost,
            'ready_time': ready_time,
            'instructions': request.POST.get('instructions', 'N/A'),
            'name': request.POST.get('name', 'Anonymous'),
            'phone': request.POST.get('phone', 'Not Provided'),
            'email': request.POST.get('email', 'Not Provided'),
        }
        return render(request, template_name, context)

    else:
        return redirect('order')