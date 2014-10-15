from django.core.urlresolvers import resolve, Resolver404
from django.conf import settings

def default(request):
    try:
        APP_NAME = resolve(request.path).app_name
        return {'APP_NAME': APP_NAME,
                'APP_INFO': dict(settings.APPS).get(APP_NAME),
                'APPS': settings.APPS}
    except Resolver404:
        return {'APPS': settings.APPS}
