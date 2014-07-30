# coding: utf-8

from django.utils.translation import ugettext as _

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render

from slasyz_ru.settings import UPLOAD_PASSWORD, MAX_FILE_SIZE
from upload.upload_files import upload_files


def upload_view(request):
    context = {'title': _('Main page'),
               'base_tpl': 'base/full.html',
               'hide_big_title': True,
               'progress_bar': True,
               'max_file_size': MAX_FILE_SIZE}

    if request.method == 'POST':
        if (request.POST.get('password') != UPLOAD_PASSWORD) and not request.user.is_authenticated():
            context['error'] = _('Incorrect password.')
        else:
            context['results'] = upload_files(request)

    return render(request, 'upload/pages/index.html', RequestContext(request, context))


def upload_ajax_view(request):
    if request.method == 'POST':
        if (request.POST.get('password') != UPLOAD_PASSWORD) and not request.user.is_authenticated():
            return render('upload/tpl/error.tpl', {'error': _('Incorrect password.')})

        results = upload_files(request)
        res = u''
        for result in results:
            res += result.render()
        return HttpResponse(res)

    return HttpResponse('', status=400)
