# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-14 19:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crudapp', '0049_auto_20161014_1511'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newusermodel',
            old_name='posts',
            new_name='test',
        ),
    ]
