# coding: utf-8

import os
from django.core.urlresolvers import reverse
from django.core.signing import BadSignature, dumps, loads


class BadIDException(Exception):
    value = "Wrong uniq ID."


class Link(object):
    def __init__(self, path):
        self.path = path

    @property
    def basename(self):
        return os.path.basename(self.path)


class FileLink(Link):
    def __init__(self, path=None, uniq_id=None):
        if not (path or uniq_id):
            raise TypeError('__init__() takes exactly 2 arguments (1 given)')
        elif path and uniq_id:
            raise TypeError('__init__() takes exactly 2 arguments (3 given)')
        elif uniq_id:
            path = self._id_to_path(uniq_id)
        super(FileLink, self).__init__(path=path)


    @property
    def public_url(self):
        url = reverse('upload:public', kwargs={'uniq_id': self.uniq_id,
                                               'basename': self.basename})
        return url


    @property
    def uniq_id(self):
        return self._path_to_id(self.path)


    @staticmethod
    def _path_to_id(path):
        return dumps(path).replace(':', '/')


    @staticmethod
    def _id_to_path(id):
        try:
            return loads(id.replace('/', ':'))
        except BadSignature:
            raise BadIDException


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
