from django.core.urlresolvers import resolve, Resolver404
from django.conf import settings


def default(request):
    try:
        app_name = resolve(request.path).app_name
        return {'APP_NAME': app_name,
                'APP_INFO': dict(settings.APPS).get(app_name),
                'APPS': settings.APPS}
    except Resolver404:
        return {'APPS': settings.APPS}
