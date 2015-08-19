# coding: utf-8

import os.path
import codecs
from datetime import datetime

from django.conf import settings
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.template.loader import render_to_string

from upload.models import File
LOG_TEMPLATE = u'[{{time}}] \033[1;{color}m{filename}\033[0m -> \033[1;36m{text}\033[0m\n'


class UploadFileResult(object):

    def __init__(self, name, text, error=False, status=200):
        self.name = name
        self.text = text
        self.error = error
        self.status = status

        if error:
            color = '32'
        else:
            color = '31'
        self._log(LOG_TEMPLATE.format(color=color, filename=name, text=text))

    def _log(self, text):
        time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        if not os.path.exists(settings.LOG_FILE):
            open(settings.LOG_FILE, 'w').close()

        with codecs.open(settings.LOG_FILE, 'a', 'utf-8') as f:
            f.write(text.format(time=time))

    def _get_short_name(self):
        filename = self.name
        if len(filename) <= 30:
            return filename
        else:
            spl = os.path.splitext(filename)
            return spl[0][:30 - 3 - 3 - len(spl[1])] + '...' + spl[0][-3:] + spl[1]

    def render_to_string(self):
        context = {'error': self.error,
                   'short_name': self._get_short_name,
                   'text': self.text}
        return render_to_string('upload/tpl/success.tpl', context)

    def render_to_response(self):
        return HttpResponse(self.render_to_string(), status=self.status)


class TooBigException(Exception):
    pass


class TeapotException(Exception):
    pass


def filepath(filename):
    return os.path.join(settings.UPLOAD_DIR, filename)


def upload_files_list(request):
    """
        Returns a list of UploadFileResult's instances.
    """
    results = []

    for uploaded_file in request.FILES.getlist('fileup'):
        try:
            # Checking file
            if uploaded_file.size > settings.MAX_FILE_SIZE:
                raise TooBigException
            if uploaded_file.name == 'error.test':
                raise TeapotException

            # trying file.ext, file_2.ext, file_3.ext, ...
            filename = uploaded_file.name
            spl = os.path.splitext(filename)
            i = 2
            while os.path.exists(filepath(filename)):
                filename = spl[0] + '_{}'.format(i) + spl[1]
                i += 1

            # copying file to destination directory
            f = open(filepath(filename), 'wb')
            f.write(uploaded_file.read())
            f.close()

            # creating database entry
            if request.user.is_authenticated():
                db_entry = File(author=request.user, filename=filename)
            else:
                db_entry = File(author=None, filename=filename)
            db_entry.save()
            link = db_entry.get_absolute_url()
            results.append(UploadFileResult(filename, link))
        except TooBigException:
            results.append(UploadFileResult(uploaded_file.name, _('File is too big.'), error=True, status=413))
        except TeapotException:
            results.append(UploadFileResult(uploaded_file.name, _('I\'m a teapot))0'), error=True, status=418))
        except:
            results.append(UploadFileResult(uploaded_file.name, _('A server error occured.'), status=500))

    return results
