from django.contrib import admin
from upload.models import File


# @admin.register(Post) # in dev-version
class FileAdmin(admin.ModelAdmin):
    ordering = ['-created']
    list_display = ['filename', 'author', 'created']


admin.site.register(File, FileAdmin)
