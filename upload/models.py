from urlparse import urljoin
from django.db import models
from django.contrib.auth.models import User

from slasyz_ru.settings import UPLOAD_URL

class File(models.Model):
    author = models.ForeignKey(User, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=255)

    def get_absolute_url(self):
        return urljoin(UPLOAD_URL, self.filename)
    get_absolute_url.short_description = 'URL'
