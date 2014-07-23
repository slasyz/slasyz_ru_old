from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class RedirectIfAnonymous:
    def process_request(self, request):
        if request.user.is_authenticated():
            if request.user.is_superuser:
                return None
        return HttpResponseRedirect(reverse('login'))
