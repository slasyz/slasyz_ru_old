from django.utils.translation import ugettext as _
from django.utils.decorators import decorator_from_middleware
from django.core.urlresolvers import reverse

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from slasyz_ru.settings import TITLE
from management.middleware import RedirectIfAnonymous


def context_processor(request):
    APP_NAME = 'management'
    return {'APP_NAME': APP_NAME,
            'APP_TITLE': TITLE[APP_NAME]}


def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(request.META['HTTP_REFERER'])

    context = {'title': _('Login'),
               'base_tpl': 'base/full.html'}
    if request.method == 'GET':
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('management'))
        else:
            return render(request, 'management/pages/login.html', RequestContext(request, context, processors=[context_processor,]))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@decorator_from_middleware(RedirectIfAnonymous)
def index(request):
    context = {'title': _('Main page'),
               'base_tpl': 'base/full.html'}
    return render(request, 'management/pages/index.html', RequestContext(request, context, processors=[context_processor,]))
