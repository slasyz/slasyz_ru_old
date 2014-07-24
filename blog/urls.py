from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('blog.views',
    url(r'^$', 'page_view', name='blog'),
    url(r'^page/(?P<page>[0-9]+)/$', 'page_view', name='blog_page'),
    url(r'^post/(?P<short_name>[a-z0-9-]+)$', 'post_view', name='blog_post'),

    url(r'^post/(?P<short_name>[a-z0-9-]+)/add_comment/$', 'add_comment_view', name='blog_add_comment'),
)
