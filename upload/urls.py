import os.path

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'upload.views.upload', name='upload'),
    url(r'^upload-ajax/$', 'upload.views.upload_ajax'),
)
