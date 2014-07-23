from django.utils.translation import ugettext as _
from django.utils.decorators import decorator_from_middleware
from django.core.urlresolvers import reverse

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render

from django.contrib.auth.models import User
from blog.models import Post
from management.forms import PostForm

from slasyz_ru.settings import TITLE
from management.middleware import RedirectIfAnonymous


def context_processor(request):
    APP_NAME = 'management'
    return {'APP_NAME': APP_NAME,
            'APP_TITLE': TITLE[APP_NAME]}


@decorator_from_middleware(RedirectIfAnonymous)
def add(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = User.objects.get(id=request.user.id)
            post.save()
            return HttpResponseRedirect(reverse('blog_post', args=[post.short_name]))
    else:
        form = PostForm()

    context = {'title': _('Adding a new post'),
               'base_tpl': 'base/full.html',
               'action': 'add',
               'form': form}
    return render(request, 'management/pages/blog/edit.html', RequestContext(request, context, processors=[context_processor,]))


@decorator_from_middleware(RedirectIfAnonymous)
def edit(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        error_text = _('There is no such post with id=={}').format(post_id)
        context = {'title': 'Oops!',
                   'base_tpl': 'base/full.html',
                   'text': error_text}
        return render(request, 'global/pages/error.html', RequestContext(request, context, processors=[context_processor,]))

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save() # check all this again. looks fine
            return HttpResponseRedirect(reverse('blog_post', args=[post.short_name]))
    else:
        form = PostForm(instance=post)

    context = {'title': _('Editing post #{}').format(post_id),
               'base_tpl': 'base/full.html',
               'action': 'edit',
               'form': form}
    return render(request, 'management/pages/blog/edit.html', RequestContext(request, context, processors=[context_processor,]))


@decorator_from_middleware(RedirectIfAnonymous)
def rm(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        error_text = _('There is no such post with id=={}').format(post_id)
        context = {'title': 'Oops!',
                   'base_tpl': 'base/full.html',
                   'text': error_text}
        return render(request, 'management/pages/error.html', RequestContext(request, context, processors=[context_processor,]))

    if request.method == 'GET':
        context = {'title': _('Removing post #{}').format(post_id),
                   'base_tpl': 'base/full.html'}
        return render(request, 'management/pages/blog/rm.html', RequestContext(request, context, processors=[context_processor,]))
    else:
        post.delete()
        return HttpResponseRedirect(reverse('blog'))


@decorator_from_middleware(RedirectIfAnonymous)
def index(request):
    context = {'title': _('Blog management main page'),
               'base_tpl': 'base/full.html'}
    return render(request, 'management/pages/blog/index.html', RequestContext(request, context, processors=[context_processor,]))

