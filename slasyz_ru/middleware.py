from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, resolve
from slasyz_ru.settings import APPS

class RedirectIfAnonymous:
    def process_request(self, request):
        url = resolve(request.path)
        APP_INFO = dict(APPS).get(url.app_name)

        if url.url_name == 'login':
            return None # do not redirect if it is a login page

        if APP_INFO:
            if APP_INFO['needs_admin']:
                if request.user.is_authenticated():
                    if not request.user.is_superuser:
                        return # error: authenticated but hasn't admin rights
                else:
                    return HttpResponseRedirect(reverse('login'))
