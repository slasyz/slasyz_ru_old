# coding: utf-8

import os
import re
from mimetypes import guess_type

from urlparse import urljoin
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render

from slasyz_ru.settings import UPLOAD_PASSWORD, MAX_FILE_SIZE, UPLOAD_DIR, UPLOAD_URL
from upload.upload_files import upload_files


@permission_required('upload.can_manage_filesystem')
def filesystem_view(request):
    path = request.GET.get('path', UPLOAD_DIR).encode('utf-8')
    if not os.path.exists(path):
        raise Http404

    if not os.path.isdir(path):
        # return content of that file
        response = HttpResponse(open(path, 'rb'))
        basename = os.path.basename(path)
        ct, encoding = guess_type(path)

        if ct is None:
            ct = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(basename)
        if encoding:
            ct = '{}; charset={}'.format(ct, encoding)
        response['Content-Type'] = ct
        return response
    else:
        dirs = []; files = []; error = ''
        try:
            for f in sorted(os.listdir(path)):
                new_path = os.path.join(path, f)
                if os.path.isdir(f):
                    dirs.append((f, new_path))
                else:
                    files.append((f, new_path))
        except OSError:
            error = _('An error occured (probably, you do not have enough rights).')

        fullpath = os.path.abspath(os.path.realpath(path)).split(os.sep)[1:]
        address_panel = [('/', '/')]

        new_path = '/'
        for i in xrange(len(fullpath)):
            new_path = os.path.join(new_path, fullpath[i])
            address_panel.append((fullpath[i], new_path))

        context = {'title': _('Filesystem manage'),
                   'base_tpl': 'base/full.html',
                   'error': error,
                   'address_panel': address_panel,
                   'dirs': dirs,
                   'files': files}
        return render(request, 'upload/pages/filesystem.html', RequestContext(request, context))


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
