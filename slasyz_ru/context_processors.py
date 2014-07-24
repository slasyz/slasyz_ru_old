from django.core.urlresolvers import resolve
from slasyz_ru.settings import INFO

def default(request):
    APP_NAME = resolve(request.path).app_name
    return {'APP_NAME': APP_NAME,
            'APP_INFO': dict(INFO).get(APP_NAME),
            'INFO': INFO}
