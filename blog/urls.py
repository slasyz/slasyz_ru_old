from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'blog.views.latest'),
    url(r'post\/(?P<post_id>\d+)', 'blog.views.post'),

    #url(r'^upload-ajax/$', 'upload.views.upload_ajax'),

    # This should be in your proxy (i.e. nginx) config
    #url(r'^static\/(?P<path>.*)$', 'django.views.static.serve', {'document_root': static(__file__)}),
)
