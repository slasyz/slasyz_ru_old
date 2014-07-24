from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, resolve
from slasyz_ru.settings import INFO

class RedirectIfAnonymous:
    def process_request(self, request):
        url = resolve(request.path)

        if url.url_name == 'login':
            return None # do not redirect if it is a login page
        if dict(INFO)[url.app_name]['needs_admin']:
            if request.user.is_authenticated():
                if not request.user.is_superuser:
                    return # error: authenticated but hasn't admin rights
            else:
                return HttpResponseRedirect(reverse('login'))
