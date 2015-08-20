# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='_text_rendered',
        ),
        migrations.RemoveField(
            model_name='post',
            name='_annotation_rendered',
        ),
        migrations.RemoveField(
            model_name='post',
            name='_full_text_rendered',
        ),
        migrations.AlterField(
            model_name='comment',
            name='author_email',
            field=models.EmailField(max_length=254, blank=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='post',
            name='annotation',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='post',
            name='full_text',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='blog.Tag', blank=True),
        ),
    ]
