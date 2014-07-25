from django.core.urlresolvers import resolve
from slasyz_ru.settings import APPS

def default(request):
    APP_NAME = resolve(request.path).app_name
    return {'APP_NAME': APP_NAME,
            'APP_INFO': dict(APPS).get(APP_NAME),
            'APPS': APPS}
