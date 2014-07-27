from django.contrib import admin
from blog.models import Post, Comment

#@admin.register(Post) # in dev-version
class PostAdmin(admin.ModelAdmin):
    ordering = ['-created']
    list_display = ['title', 'author', 'created', 'is_draft', 'get_absolute_url', 'get_comments_count', 'annotation']
    actions = ['make_published']

    def make_published(self, request, queryset):
        queryset.update(is_draft=False)
    make_published.short_description = "Mark selected posts as published"


class CommentAdmin(admin.ModelAdmin):
    ordering = ['created']
    list_display = ['post', 'author', 'author_name', 'created', 'get_absolute_url', 'text']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
