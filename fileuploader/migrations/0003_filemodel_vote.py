# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-05 12:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileuploader', '0002_filemodel_upload'),
    ]

    operations = [
        migrations.AddField(
            model_name='filemodel',
            name='vote',
            field=models.IntegerField(default=0),
        ),
    ]