from django.db import models
from django.contrib.auth.models import User
from html import escape
from re import sub

from django.core.validators import RegexValidator
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.utils.encoding import python_2_unicode_compatible

from blog.urls import SHORT_NAME_REGEX
short_name_validator = RegexValidator('^{}$'.format(SHORT_NAME_REGEX),
                                      _('Short name should consist of small latin letters and dash.'))
tag_name_validator = RegexValidator(r'^[^/]+$', _('Tag name should not contain slash symbol.'))


@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=255, validators=[tag_name_validator])

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Post(models.Model):
    author = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    short_name = models.CharField(max_length=255, unique=True, validators=[short_name_validator])
    tags = models.ManyToManyField(Tag, blank=True)
    is_draft = models.BooleanField(default=False, verbose_name=u'Draft')
    title = models.CharField(max_length=255)
    annotation = models.TextField()
    full_text = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post', args=[self.id, self.short_name])
    get_absolute_url.short_description = 'URL'

    def get_comments_count(self):
        return Comment.objects.filter(post_id=self.id).count()
    get_comments_count.short_description = 'comments'

    class Meta:
        permissions = (
            ("can_read_drafts", "Can read draft posts"),
        )


class Comment(models.Model):
    author = models.ForeignKey(User, null=True, blank=True)
    author_name = models.CharField(max_length=60, blank=True)
    author_email = models.EmailField(blank=True)
    post = models.ForeignKey(Post)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        post = Post.objects.get(id=self.post_id)
        return '{}#comment-{}'.format(post.get_absolute_url(), self.id)
    get_absolute_url.short_description = 'URL'

    def get_formatted_text(self):
        text = escape(self.text)
        text = sub(r'(?:https?|s?ftps?)://([^/]+)[^\"\s]+', '<a href="\g<0>">\g<1></a>', text)
        return text
