# coding: utf-8

import os.path
import json
import datetime
from django.http import HttpResponse

from django.template.loader import get_template
from django.template import RequestContext
from django.shortcuts import render

from upload.forms import UploadFileForm
from slasyz_ru.settings import UPLOAD_DIR, UPLOAD_URL, MAX_FILE_SIZE, UPLOAD_PASSWORD, LOG_FILE
LOG_TEMPLATE = '[{{time}}] \033[1;{color}m{filename}\033[0m -> \033[1;36m{text}\033[0m\n'

class LinkResult(dict):
    def __init__(self, name, link):
        self['name'] = name
        self['short_name'] = get_short_name(name)
        self['link'] = link
        self['status'] = 200
        log(LOG_TEMPLATE.format(color='32', filename=name, text=link))

class ErrorResult(dict):
    def __init__(self, error, name='', status=500):
        self['error'] = error
        self['status'] = status
        if name:
            self['name'] = name
            self['short_name'] = get_short_name(name)
        else:
            name = '(upload error)'
        log(LOG_TEMPLATE.format(color='31', filename=name, text=error))


def filepath(filename):
    return os.path.join(UPLOAD_DIR, filename)


def get_short_name(filename):
    if len(filename) <= 30:
        return filename
    else:
        spl = os.path.splitext(filename)
        return spl[0][:30-3-3-len(spl[1])] + '...' + spl[0][-3:] + spl[1]


def log(text):
    time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    if not os.path.exists(LOG_FILE): open(LOG_FILE, 'w').close()

    f = open(LOG_FILE, 'a')
    f.write(text.format(time=time))
    f.close()


def upload_file(request, uploaded_file):
    from urlparse import urljoin
    try:
        # Checking file
        if uploaded_file.size > MAX_FILE_SIZE:
            return ErrorResult('File is too big.', name=uploaded_file.name, status=413)
        if uploaded_file.name == 'error.test':
            return ErrorResult('I\'m a teapot)))0', name=uploaded_file.name, status=418)

        # trying file.ext, file_2.ext, file_3.ext, ...
        filename = uploaded_file.name
        spl = os.path.splitext(filename)
        i = 2
        while os.path.exists(filepath(filename)):
            filename = spl[0] + ('_%i' % i) + spl[1]
            i+=1

        # copying file to destination directory
        f = open(filepath(filename), 'w')
        f.write(uploaded_file.read())
        f.close()

        link = urljoin(UPLOAD_URL, filename)
        return LinkResult(filename, link)
    except:
        return ErrorResult('A server error occured.', name=uploaded_file.name, status=500)


def upload(request):
    context = {'base_tpl': 'base/full.html',
               'hide_big_title': True,
               'progress_bar': True,
               'max_file_size': MAX_FILE_SIZE}
    files = [] # TODO: rewrite this
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if not form.is_valid():
            files.append(ErrorResult('An error occured.', status=400))
        elif (request.POST.get('password') != UPLOAD_PASSWORD) and not request.user.is_authenticated():
            files.append(ErrorResult('Incorrect password', status=403))
        else:
            for f in request.FILES.getlist('fileup'):
                result = upload_file(request, f)
                files.append(result)

    context['files'] = files
    return render(request, 'upload/pages/index.html', RequestContext(request, context))


def upload_ajax(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if not form.is_valid():
            return HttpResponse(json.dumps(ErrorResult('An error occured.', status=400)), status=400)
        if (request.POST.get('password') != UPLOAD_PASSWORD) and not request.user.is_authenticated():
            return HttpResponse(json.dumps(ErrorResult('Incorrect password.', status=403)), status=403)

        result = upload_file(request, request.FILES['fileup'])
        return HttpResponse(json.dumps(result), status=result['status'])
    else:
        return HttpResponse(json.dumps(ErrorResult('Should be POST-request.', status=400)), status=400)
