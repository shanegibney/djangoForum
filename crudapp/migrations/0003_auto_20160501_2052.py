# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-01 20:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crudapp', '0002_auto_20160501_1701'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postmodel',
            old_name='blah',
            new_name='topic',
        ),
        migrations.AddField(
            model_name='topicmodel',
            name='topic_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]