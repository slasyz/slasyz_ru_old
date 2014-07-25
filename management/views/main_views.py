from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from management.middleware import RedirectIfAnonymous


def index(request):
    context = {'title': _('Main page'),
               'base_tpl': 'base/full.html'}
    return render(request, 'management/pages/index.html', RequestContext(request, context))
