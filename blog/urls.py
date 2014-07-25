from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

SHORT_NAME_REGEX = '[a-z0-9-]+'

urlpatterns = patterns('blog.views',
    url(r'^$', 'page_view', name='blog'),
    url(r'^page/(?P<page>[0-9]+)/$', 'page_view', name='blog_page'),
    url(r'^post/(?P<post_id>[0-9]+)-(?P<short_name>{})$'.format(SHORT_NAME_REGEX), 'post_view', name='blog_post'),

    url(r'^post/(?P<post_id>[0-9]+)-(?P<short_name>{})/add_comment/$'.format(SHORT_NAME_REGEX), 'add_comment_view', name='blog_add_comment'),
)
