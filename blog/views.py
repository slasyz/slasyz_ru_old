# coding: utf-8

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage

from slasyz_ru.settings import POSTS_PER_PAGE
from blog.models import Post, Comment
from blog.forms import CommentForm, AnonymousCommentForm
from management.views import blog_views


def page_view(request, page=1):
    posts_all = Post.objects.all().order_by('-created')
    paginator = Paginator(posts_all, POSTS_PER_PAGE)

    try:
        current_page = paginator.page(page)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        current_page = paginator.page(paginator.num_pages)

    prev_page = next_page = 0
    if current_page.has_previous():
        prev_page = current_page.previous_page_number()
    if current_page.has_next():
        next_page = current_page.next_page_number()

    if page == 1:
        title = _('Latest')
    else:
        title = _('Page {}').format(page)


    context = {'title': title,
               'base_tpl': 'base/full.html',
               'posts': current_page,
               'prev_page': prev_page,
               'next_page': next_page}
    return render(request, 'blog/pages/posts.html', RequestContext(request, context))


def post_view(request, post_id, short_name):
    try:
        res = Post.objects.get(id=post_id, short_name=short_name)
    except Post.DoesNotExist:
        raise Http404()
    comments = Comment.objects.filter(post_id=res.id).order_by('created')

    if request.user.is_authenticated():
        comment_form = CommentForm()
    else:
        comment_form = AnonymousCommentForm()

    context = {'title': res.title,
               'base_tpl': 'base/full.html',
               'post': res,
               'comments': comments,
               'comment_form': comment_form}

    return render(request, 'blog/pages/post.html', RequestContext(request, context))


def add_comment_view(request, post_id, short_name):
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=post_id, short_name=short_name)
        except Post.DoesNotExist:
            raise Http404()

        ### TODO:
        # избавиться от копипаста
        if request.user.is_authenticated():
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.post = post
                comment.save()
        else:
            form = AnonymousCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = None
                comment.post = post
                comment.save()
    
    return HttpResponseRedirect(reverse('blog_post', args=[short_name,]))
