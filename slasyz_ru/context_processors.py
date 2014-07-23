from django.core.urlresolvers import resolve
from slasyz_ru.settings import TITLE, LINKS

def default(request):
    APP_NAME = resolve(request.path).app_name
    return {'APP_NAME': APP_NAME,
            'APP_TITLE': TITLE[APP_NAME],
            'TOPBAR_LINKS': LINKS.get(APP_NAME)}
