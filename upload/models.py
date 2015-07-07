from urllib.parse import urljoin

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class File(models.Model):
    author = models.ForeignKey(User, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=255)

    def get_absolute_url(self):
        return urljoin(settings.UPLOAD_URL, self.filename)
    get_absolute_url.short_description = 'URL'

    class Meta:
        permissions = (
            ("can_manage_filesystem", "Can manage filesystem"),
        )
