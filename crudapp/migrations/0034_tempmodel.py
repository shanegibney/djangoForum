# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-19 12:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crudapp', '0033_auto_20160618_2000'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topicid', models.IntegerField(default=0)),
                ('date', models.DateTimeField(verbose_name='date published')),
                ('author', models.CharField(max_length=30)),
            ],
        ),
    ]
