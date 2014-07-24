from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

blog_patterns = patterns('management.views.blog_views',
    url(r'^$', 'index', name='management_blog'),

    url(r'^add\/$', 'add', name='management_blog_add'),
    url(r'^edit/(?P<post_id>[0-9]+)\/?$', 'edit', name='management_blog_edit'),
    url(r'^rm/(?P<post_id>[0-9]+)\/?$', 'rm', name='management_blog_rm'),
)

urlpatterns = patterns('management.views.main_views',
    url(r'^$', 'index', name='management'),
    url(r'^login/$', 'login_view', name='login'),
    url(r'^logout/$', 'logout_view', name='logout'),

    url(r'^blog/', include(blog_patterns)),
)
