import os
import time

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from slasyz_ru.settings import STATIC_ROOT, STATIC_URL


def login_view(request):
    context = {'title': _('Login'),
               'base_tpl': 'base/full.html'}

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return # TODO: error output
    else:
        if request.user.is_authenticated():
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('index')))
        else:
            return render(request, 'global/pages/login.html', RequestContext(request, context))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('index')))


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
