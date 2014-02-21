from django.http import HttpResponse
from django.template.loader import get_template
from django.template import RequestContext
from django.shortcuts import render

def latest(request):
    posts = [{'title': 'Hello World',
              'created': '2014-02-21 11:00:00',
              'text': '<p>This is text of post</p><p>This is another line of text of post. This is another sentence of another line of text of post.</p>'},
             {'title': 'Hello World 2',
              'created': '2014-02-21 10:00:00',
              'text': '<p>This is text of post</p><p>This is another line of text of post. This is another sentence of another line of text of post.</p>'}]
    context = {'posts': posts, 'title': 'Latest posts', 'base_tpl': 'blog/base.html'}
    return HttpResponse(render(request, 'blog/posts.html', RequestContext(request, context)))