from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest

# Create your views here.

def show_form(request: HttpRequest):
    '''Returns a simple response to the request'''

    template_name = 'formdata/form.html'

    return render(request, template_name)

def submit(request: HttpRequest):
    '''Handles form submission'''

    if request.POST:
        template_name = 'formdata/submit.html'
        context = {
            'name': request.POST.get('name', 'Anonymous'),
            'color': request.POST.get('color', 'Black')
        }
        return render(request, template_name, context)

    else:
        return redirect('show_form')