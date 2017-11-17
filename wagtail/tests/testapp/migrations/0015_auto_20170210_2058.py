# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-10 11:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import wagtail.images.models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0014_event_categories'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomRendition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filter_spec', models.CharField(db_index=True, max_length=255)),
                ('file', models.ImageField(height_field='height', upload_to=wagtail.images.models.get_rendition_upload_to, width_field='width')),
                ('width', models.IntegerField(editable=False)),
                ('height', models.IntegerField(editable=False)),
                ('focal_point_key', models.CharField(blank=True, default='', editable=False, max_length=16)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='renditions', to='tests.CustomImage')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='customrendition',
            unique_together=set([('image', 'filter_spec', 'focal_point_key')]),
        ),
    ]
