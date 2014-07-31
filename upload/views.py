# coding: utf-8

import os
import re
import string
from mimetypes import guess_type
from itertools import chain
from string import ascii_letters
from random import choice

from urlparse import urljoin
from django.utils.translation import ugettext as _
from django.core.signing import Signer, BadSignature
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, StreamingHttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render

from slasyz_ru.settings import UPLOAD_PASSWORD, MAX_FILE_SIZE, UPLOAD_DIR, UPLOAD_URL
from upload.upload_files import upload_files


class Link(object):
    def __init__(self, path):
        self.path = path

    @property
    def basename(self):
        return os.path.basename(self.path)


class FileLink(Link):
    @property
    def signature(self):
        signer = Signer()
        sign = signer.sign(self.path).split(':')[1]
        print ">>>>", sign
        return sign


class DirectoryLink(Link):
    @property
    def basename(self):
        if self.path == '/':
            return '/'
        elif self.path[-1] == '/':
            return os.path.basename(self.path[:-1])
        else:
            return os.path.basename(self.path)


def read_in_ranges(file_object, ranges, file_size, boundary, content_type=None):
    for r in ranges:
        a, b = r
        yield '--{}\r\n'.format(boundary)
        if content_type: yield 'Content-Type: {}\r\n'.format(content_type)
        yield 'Content-Range: {}-{}/{}\r\n'.format(a, b, file_size)
        yield '\r\n'

        for chunk in read_in_chunks(file_object, a, b):
            yield chunk
        yield '\r\n'
    yield '--{}--'.format(boundary)


def read_in_chunks(file_object, beg, end, chunk_size=1024):
    """
    Iterate file part piece by piece.
    """

    file_object.seek(beg)
    while True:
        chunk = min(chunk_size, end-file_object.tell()+1)
        data = file_object.read(chunk)
        if not data: return
        yield data


def filestream_view(request, path):
    """
    Stream content of file located on "path".
    """
    f = open(path, 'rb')
    basename = os.path.basename(path)
    size = os.path.getsize(path)
    ct, encoding = guess_type(path)
    content_range = request.META.get('HTTP_RANGE')
    if ct is None: ct = 'application/octet-stream'

    if content_range:
        # "Range" header parsing
        # Valid examples:
        # > Range: bytes=a-b             // return bytes from a to b
        # > Range: bytes=a-              // return bytes from a to end of file
        # > Range: bytes=-b              // return last b bytes
        # > Range: bytes=a1-b1,a2-b2,... // return bytes from a1 to b1, from a2 to b2 etc

        ranges = [] # list of non-empty ranges
        raw_ranges = re.match(r'^bytes=(?P<ranges>(\d*-\d*,)*(\d*-\d*))$', content_range).group('ranges')

        for r in raw_ranges.split(','):
            a, b = r.split('-')
            if (a != '') and (b != ''):
                a, b = int(a), int(b)
            elif b == '':
                a, b = int(a), size - 1
            elif a == '':
                a, b = size-int(b), size-1
            if b >= size: b = size - 1

            if b-a >= 0:
                a_real, b_real = a, b
                ranges.append((a, b))

        if len(ranges) == 0:
            return HttpResponse(status=416)
        elif len(ranges) == 1:
            ### Only one range.
            # HTTP 206 Partial Content
            # Content-Type = (content type of file)
            # Content-Length = (range size)
            # Content-Range = (range range)
            #
            # (range data)
            a, b = a_real, b_real
            response = StreamingHttpResponse(read_in_chunks(f, a, b), status=206)
            response['Content-Length'] = b - a + 1
            response['Content-Range'] = 'bytes {}-{}/{}'.format(a, b, size)
        else:
            ### Several ranges.
            # > HTTP 206 Partial Content
            # > Content-Type = multipart/byteranges; boundary=BOUNDARY
            # >
            # > --BOUNDARY
            # > Content-Type: (content type of file)
            # > Content-Range: (range_1 range)
            # >
            # > (range_1 data)
            # > --BOUNDARY
            # > Content-Type: (content type of file)
            # > Content-Range: (range_2 range)
            # >
            # > (range_2 data)
            # > (et cetera)
            # > --BOUNDARY--

            # There is one pretty unlikely, but possible situation,
            # when file (one of range to be specific) contains boundary.
            boundary = ''.join(choice(ascii_letters+'_') for x in range(50))
            response = StreamingHttpResponse(read_in_ranges(f, ranges, size, boundary=boundary, content_type=ct), status=206)
            ct = 'multipart/byteranges; boundary={}'
    else:
        response = StreamingHttpResponse(read_in_chunks(f, 0, size), status=200)
        response['Content-Length'] = size

    if encoding: response['Content-Encoding'] = encoding
    response['Content-Type'] = ct

    return response


def public_view(request, path):
    signer = Signer()
    try:
        value = '{}:{}'.format(path, request.GET.get('signature'))
        signer.unsign(value)
        return filestream_view(request, path)
    except BadSignature:
        raise PermissionDenied


@login_required()
@permission_required('upload.can_manage_filesystem', raise_exception=True)
def filesystem_view(request):
    path = request.GET.get('path', UPLOAD_DIR).encode('utf-8')
    if not os.path.exists(path):
        raise Http404

    if not os.path.isdir(path):
        # return content of that file
        return filestream_view(request, path)
    else:
        dirs = []; files = []; error = ''
        try:
            for f in sorted(os.listdir(path)):
                new_path = os.path.join(path, f)
                if os.path.isdir(os.path.join(path, f)):
                    dirs.append(DirectoryLink(new_path))
                else:
                    files.append(FileLink(new_path))
        except OSError:
            error = _('An error occured (probably, you do not have enough rights).')

        fullpath = os.path.abspath(os.path.realpath(path)).split(os.sep)[1:]
        address_panel = [DirectoryLink('/')]

        new_path = '/'
        for i in xrange(len(fullpath)):
            new_path = os.path.join(new_path, fullpath[i])
            address_panel.append(DirectoryLink(new_path))

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
