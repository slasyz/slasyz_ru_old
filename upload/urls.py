from django.conf.urls import patterns, include, url

urlpatterns = patterns('upload.views',
    url(r'^$', 'upload_view', name='upload'),
    url(r'^upload-ajax/$', 'upload_ajax_view'),

    url(r'^filesystem/', 'filesystem_view', name='upload_filesystem'),
    url(r'^public/(?P<uniq_id>.+)/(?P<basename>[^/]+)$', 'public_view', name='upload_public'),
)
