from django.core.urlresolvers import resolve, Resolver404
from slasyz_ru.settings import APPS

def default(request):
    try:
        APP_NAME = resolve(request.path).app_name
        return {'APP_NAME': APP_NAME,
                'APP_INFO': dict(APPS).get(APP_NAME),
                'APPS': APPS}
    except Resolver404:
        return {'APPS': APPS}
