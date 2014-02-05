# coding: utf-8

from django.conf.urls import patterns, include, url

# по идее, эта херня должна дублироваться в конфигах апача-нджинкса-чтонибудьещё

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'slasyz_ru.views.home', name='home'),
    # url(r'^slasyz_ru/', include('slasyz_ru.foo.urls')),

    url(r'^$', 'slasyz_ru.views.index'),
    url(r'^upload/', include('upload.urls')),

    # This should be in your proxy (i.e. nginx) config
    url(r'^static\/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/sl/programming/django/slasyz_ru/slasyz_ru/static'}),
)
