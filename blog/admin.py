from django.contrib import admin
from blog.models import Post

#@admin.register(Post) # in dev-version
class PostAdmin(admin.ModelAdmin):
    ordering = ['-created']
    list_display = ['title', 'author', 'created', 'get_absolute_url', 'get_comments_count', 'annotation']

admin.site.register(Post, PostAdmin)
