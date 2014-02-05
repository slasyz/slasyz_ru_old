# coding: utf-8

import os.path
import json
from django.http import HttpResponse

from django.template.loader import get_template
from django.template import RequestContext
from django.shortcuts import render

from upload.forms import UploadFileForm
from slasyz_ru.settings import UPLOAD_DIR, UPLOAD_URL, MAX_FILE_SIZE, UPLOAD_PASSWORD

def filepath(filename):
    return os.path.join(UPLOAD_DIR, filename)

def upload_file(uploaded_file):
    from urlparse import urljoin
    try:
        # Checking file
        if uploaded_file.size > MAX_FILE_SIZE:
            return {'error': 'File is too big.', 'status': 413}
        if uploaded_file.name == 'error.test':
            return {'error': 'I\'m a teapot)))0', 'status': 418}

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
        result = {'link': link,
                  'status': 200}
        return result
    except:
        return {'error': 'A server error occured', 'status': 500}

def upload(request):
    context = {'max_file_size': MAX_FILE_SIZE}
    files = []
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if not form.is_valid():
            files.append({'error': 'An error occured.', 'status': 400})
        elif request.POST['password'] != UPLOAD_PASSWORD:
            files.append({'error': 'Incorrect password.', 'status': 403})
        else:
            for f in request.FILES.getlist('fileup'):
                result = upload_file(f)
                files.append(result)

    context['files'] = files
    return HttpResponse(render(request, 'upload/upload.html', RequestContext(request, context)))

def upload_ajax(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if not form.is_valid():
            return HttpResponse(json.dumps({'error': 'An error occured.', 'status': 400}), status=400)
        if request.POST['password'] != UPLOAD_PASSWORD:
            return HttpResponse(json.dumps({'error': 'Incorrect password.', 'status': 403}), status=403)

        result = upload_file(request.FILES['fileup'])
        return HttpResponse(json.dumps(result), status=result['status'])
    else:
        return HttpResponse(json.dumps({'error': 'Should be POST-request.'}), status=400)
