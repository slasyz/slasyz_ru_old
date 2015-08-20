# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import precise_bbcode.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author_name', models.CharField(max_length=60, blank=True)),
                ('author_email', models.EmailField(max_length=75, blank=True)),
                ('_text_rendered', models.TextField(null=True, editable=False, blank=True)),
                ('text', precise_bbcode.fields.BBCodeTextField(no_rendered_field=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('short_name', models.CharField(unique=True, max_length=255, validators=[django.core.validators.RegexValidator(r'^[a-z0-9-]+$', 'Short name should consist of small latin letters and dash.')])),
                ('is_draft', models.BooleanField(default=False, verbose_name='Draft')),
                ('title', models.CharField(max_length=255)),
                ('_annotation_rendered', models.TextField(null=True, editable=False, blank=True)),
                ('annotation', precise_bbcode.fields.BBCodeTextField(no_rendered_field=True)),
                ('_full_text_rendered', models.TextField(null=True, editable=False, blank=True)),
                ('full_text', precise_bbcode.fields.BBCodeTextField(no_rendered_field=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('can_read_drafts', 'Can read draft posts'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(r'^[^/]+$', 'Tag name should not contain slash symbol.')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='blog.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(to='blog.Post'),
            preserve_default=True,
        ),
    ]
