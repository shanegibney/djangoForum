# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-18 19:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('crudapp', '0031_auto_20160618_1923'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='infomodel',
            name='date_pub',
        ),
        migrations.AddField(
            model_name='infomodel',
            name='datepub',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 18, 19, 26, 6, 839969, tzinfo=utc), verbose_name='datepub'),
            preserve_default=False,
        ),
    ]
