import os
import time

from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render
from django.http import HttpResponse

from slasyz_ru.settings import STATIC_ROOT

def index(request):
    backgrounds = os.listdir(os.path.join(STATIC_ROOT, 'backgrounds'))
    backgrounds.sort()
    n = len(backgrounds)
    i = int(time.time()) // (60*60*24) % n

    return HttpResponse(render(request, 'index.html', {'background': backgrounds[i]}))

def custom_400(request):
    return HttpResponse(render(request, 'error.html', {'code': 400, 'name': 'Bad Request'}), status=400)

def custom_403(request):
    return HttpResponse(render(request, 'error.html', {'code': 403, 'name': 'Forbidden'}), status=403)

def custom_404(request):
    return HttpResponse(render(request, 'error.html', {'code': 404, 'name': 'Not Found'}), status=404)

def custom_500(request):
    return HttpResponse(render(request, 'error.html', {'code': 500, 'name': 'Internal Server Error'}), status=500)
