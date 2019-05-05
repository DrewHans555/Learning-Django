from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic


def index(request):
    template = 'pages/index.html'
    return render(request, template)
