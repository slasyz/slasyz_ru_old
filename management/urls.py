from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

blog_patterns = patterns('',
    url(r'^$', 'management.views.blog_views.index', name='management_blog'),

    url(r'^add\/$', 'management.views.blog_views.add', name='management_blog_add'),
    url(r'^edit/(?P<post_id>[0-9]+)\/?$', 'management.views.blog_views.edit', name='management_blog_edit'),
    url(r'^rm/(?P<post_id>[0-9]+)\/?$', 'management.views.blog_views.rm', name='management_blog_rm'),
)

urlpatterns = patterns('',
    url(r'^$', 'management.views.main_views.index', name='management'),
    url(r'^login/$', 'management.views.main_views.login_view', name='login'),
    url(r'^logout/$', 'management.views.main_views.logout_view', name='logout'),

    url(r'^blog/', include(blog_patterns)),
)
