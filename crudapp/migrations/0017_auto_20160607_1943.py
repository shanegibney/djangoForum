# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-07 19:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crudapp', '0016_infomodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='infomodel',
            name='user',
            field=models.CharField(default='lile', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='blogmodel',
            name='vote',
            field=models.IntegerField(default=0, max_length=3),
        ),
    ]
