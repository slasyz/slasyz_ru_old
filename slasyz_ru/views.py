import datetime
from django.http import HttpResponse

from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render

def index(request):
	from random import choice

	bgcolors =   ('#002', '#020', '#200', '#202', '#022', '#222')
	textcolors = ('#bbf', '#bfb', '#fbb', '#fbf', '#bff', '#bbb')

	color = {'background': choice(bgcolors), 'text': choice(textcolors)}
	return HttpResponse(render(request, 'index.html', {'color': color}))

def custom_400(request):
    return HttpResponse(render(request, 'error.html', {'code': 400, 'name': 'Bad Request'}), status=400)

def custom_403(request):
    return HttpResponse(render(request, 'error.html', {'code': 403, 'name': 'Forbidden'}), status=403)

def custom_404(request):
    return HttpResponse(render(request, 'error.html', {'code': 404, 'name': 'Not Found'}), status=404)

def custom_500(request):
    return HttpResponse(render(request, 'error.html', {'code': 500, 'name': 'Internal Server Error'}), status=404)
