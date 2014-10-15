# coding: utf-8

from django.conf import settings
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage

from blog.models import Tag, Post, Comment
from blog.forms import CommentForm, AnonymousCommentForm


def get_page(queryset, page, page_func):
    paginator = Paginator(queryset, settings.POSTS_PER_PAGE)

    try:
        current_page = paginator.page(page)
    except EmptyPage:
        # If page is out of range (e.g. 9999), redirect to last available page.
        return HttpResponseRedirect(page_func(paginator.num_pages))

    prev_page = next_page = 0
    if current_page.has_previous():
        prev_page = current_page.previous_page_number()
    if current_page.has_next():
        next_page = current_page.next_page_number()

    prev_page_url = next_page_url = None
    if prev_page: prev_page_url = page_func(prev_page)
    if next_page: next_page_url = page_func(next_page)

    return current_page, prev_page_url, next_page_url


# TODO: rewrite this and next view
def page_view(request, page=1):
    main_page = reverse('blog')
    if (int(page) == 1) and (request.path != main_page):
        return HttpResponseRedirect(main_page)

    posts_all = Post.objects.all().order_by('-created')
    if not request.user.has_perm('post.can_read_drafts'):
        posts_all = posts_all.filter(is_draft=False)

    res = get_page(posts_all, page, lambda x: reverse('blog_page', args=[x]))
    try:
        current_page, prev_page_url, next_page_url = res
    except ValueError:
        return res

    if page == 1:
        title = _('Latest')
    else:
        title = _('Page {}').format(page)

    context = {'title': title,
               'base_tpl': 'base/full.html',
               'posts': current_page,
               'prev_page_url': prev_page_url,
               'next_page_url': next_page_url}
    return render(request, 'blog/pages/posts.html', context)


# TODO: rewrite this and previous view
def tag_page_view(request, tag_name, page=1):
    main_page = reverse('blog_tag', args=[tag_name,])
    if (int(page) == 1) and (request.path != main_page):
        return HttpResponseRedirect(main_page)

    try:
        tag = Tag.objects.get(name=tag_name)
    except Tag.DoesNotExist:
        raise Http404

    posts_all = Post.objects.filter(tags__id=tag.id)
    if not request.user.has_perm('post.can_read_drafts'):
        posts_all = posts_all.filter(is_draft=False)

    res = get_page(posts_all, page, lambda x: reverse('blog_tag_page', args=[tag_name, x]))
    try:
        current_page, prev_page_url, next_page_url = res
    except ValueError:
        return res

    title = _('Tag "{}" - page {}').format(tag_name, page)
    context = {'title': title,
               'base_tpl': 'base/full.html',
               'posts': current_page,
               'prev_page_url': prev_page_url,
               'next_page_url': next_page_url}
    return render(request, 'blog/pages/posts.html', context)

def post_view(request, post_id, short_name):
    try:
        res = Post.objects.get(id=post_id, short_name=short_name)
    except Post.DoesNotExist:
        raise Http404

    if res.is_draft and not request.user.has_perm('post.can_read_drafts'):
        raise Http404

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

    return render(request, 'blog/pages/post.html', context)


def add_comment_view(request, post_id, short_name):
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=post_id, short_name=short_name)
        except Post.DoesNotExist:
            raise Http404

        ### TODO: do something with this copypaste
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
    
    return HttpResponseRedirect(reverse('blog_post', args=[post_id, short_name,]))
