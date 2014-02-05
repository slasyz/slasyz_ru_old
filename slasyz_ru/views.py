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
