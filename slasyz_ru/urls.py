# coding: utf-8

import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

# по идее, эта херня должна дублироваться в конфигах апача-нджинкса-чтонибудьещё

handler400 = 'slasyz_ru.views.custom_400'
handler403 = 'slasyz_ru.views.custom_403'
handler404 = 'slasyz_ru.views.custom_404'
handler500 = 'slasyz_ru.views.custom_500'

urlpatterns = patterns('',
    url(r'^$', 'slasyz_ru.views.index', name='index'),
    url(r'^upload/', include('upload.urls', app_name='upload')),
    url(r'^blog/', include('blog.urls', app_name='blog')),
    url(r'^management/', include('management.urls', app_name='management')),

    url(r'^400$', handler400),
    url(r'^403$', handler403),
    url(r'^404$', handler404),
    url(r'^500$', handler500),

    # This should be in your proxy (i.e. nginx) config
    #url(r'^static\/(?P<path>.*)$', 'django.views.static.serve', {'document_root': static(__file__)}),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
