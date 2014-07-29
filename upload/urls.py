from django.conf.urls import patterns, include, url

urlpatterns = patterns('upload.views',
    url(r'^$', 'upload_view', name='upload'),
    url(r'^upload-ajax/$', 'upload_ajax_view'),
)
