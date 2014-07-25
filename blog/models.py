from django.db import models
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse


class Post(models.Model):
    author = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    short_name = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    annotation = models.TextField()
    full_text = models.TextField()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_post', args=[self.id, self.short_name])
    get_absolute_url.short_description = 'URL'

    def get_comments_count(self):
        return Comment.objects.filter(post_id=self.id).count()
    get_comments_count.short_description='comments'


class Comment(models.Model):
    author = models.ForeignKey(User, null=True, blank=True)
    author_name = models.CharField(max_length=60, blank=True)
    author_email = models.EmailField(blank=True)
    post = models.ForeignKey(Post)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        post = Post.objects.get(id=self.post_id)
        return '{}#comment-{}'.format(reverse('blog_post', args=[post.short_name,]), self.id)
