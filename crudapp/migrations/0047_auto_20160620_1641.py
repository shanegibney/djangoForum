# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-20 16:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crudapp', '0046_auto_20160620_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogmodel',
            name='categories',
            field=models.CharField(choices=[('GH', 'General Help'), ('SP', 'Submitting Portfolios'), ('GT', 'General Teaching'), ('L12', 'Level 1 & 2'), ('L3', 'Level 3'), ('L4', 'Level 4'), ('L5', 'Level 5'), ('L6', 'Level 6')], default='L4', max_length=30),
        ),
        migrations.AlterField(
            model_name='topicmodel',
            name='categories',
            field=models.CharField(choices=[('GH', 'General Help'), ('SP', 'Submitting Portfolios'), ('GT', 'General Teaching'), ('L12', 'Level 1 & 2'), ('L3', 'Level 3'), ('L4', 'Level 4'), ('L5', 'Level 5'), ('L6', 'Level 6')], default='L4', max_length=30),
        ),
    ]