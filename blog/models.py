from django.db import models
from django.contrib.auth.models import User
from precise_bbcode.fields import BBCodeTextField

from django.core.validators import RegexValidator
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from blog.urls import SHORT_NAME_REGEX
short_name_validator = RegexValidator('^{}$'.format(SHORT_NAME_REGEX), _('Short name should consist of small latin letters and dash.'))

class Post(models.Model):
    author = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    short_name = models.CharField(max_length=255, unique=True, validators=[short_name_validator,])
    is_draft = models.BooleanField(default=False, verbose_name=u'Draft')
    title = models.CharField(max_length=255)
    annotation = BBCodeTextField()
    full_text = BBCodeTextField()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_post', args=[self.id, self.short_name])
    get_absolute_url.short_description = 'URL'

    def get_comments_count(self):
        return Comment.objects.filter(post_id=self.id).count()
    get_comments_count.short_description = 'comments'


class Comment(models.Model):
    author = models.ForeignKey(User, null=True, blank=True)
    author_name = models.CharField(max_length=60, blank=True)
    author_email = models.EmailField(blank=True)
    post = models.ForeignKey(Post)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        post = Post.objects.get(id=self.post_id)
        return '{}#comment-{}'.format(reverse('blog_post', args=[post.id, post.short_name]), self.id)
    get_absolute_url.short_description = 'URL'
