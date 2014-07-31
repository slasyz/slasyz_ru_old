import os
import time

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.utils.six.moves.urllib.parse import urlparse

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render

from django.contrib.auth.views import login
from django.contrib.auth import logout

from slasyz_ru.settings import STATIC_ROOT, STATIC_URL


def login_view(request):
    context = {'title': _('Login'),
               'base_tpl': 'base/full.html'}
    return login(request, 'global/pages/login.html', extra_context=context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('index')))


def error_view(request, error='Unknown error'):
    context = {'title': 'Error!',
               'base_tpl': 'base/full.html',
               'error': error}
    return render(request, 'global/pages/error.html', RequestContext(request, context))


def index(request):
    files = os.listdir(os.path.join(STATIC_ROOT, 'backgrounds'))

    backgrounds = [os.path.join(STATIC_URL, 'backgrounds', x) for x in files]
    backgrounds.sort()

    wp_list = ', '.join(['"url({})"'.format(x) for x in backgrounds])
    i = int(time.time()) // (60*60*24) % len(backgrounds)

    return HttpResponse(render(request, 'index.html', {'background': backgrounds[i],
                                                       'index': i,
                                                       'wp_list': wp_list}))


def custom_400(request):
    return HttpResponse(render(request, 'error.html', {'code': 400, 'name': 'Bad Request'}), status=400)

def custom_403(request):
    return HttpResponse(render(request, 'error.html', {'code': 403, 'name': 'Forbidden'}), status=403)

def custom_404(request):
    return HttpResponse(render(request, 'error.html', {'code': 404, 'name': 'Not Found'}), status=404)

def custom_500(request):
    return HttpResponse(render(request, 'error.html', {'code': 500, 'name': 'Internal Server Error'}), status=500)
