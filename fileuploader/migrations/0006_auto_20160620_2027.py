# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-20 20:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileuploader', '0005_filemodel_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filemodel',
            name='categories',
            field=models.CharField(choices=[('GH', 'General Help'), ('SP', 'Submitting Portfolios'), ('GT', 'General Teaching'), ('L12', 'Level 1 & 2'), ('L3', 'Level 3'), ('L4', 'Level 4'), ('L5', 'Level 5'), ('L6', 'Level 6')], default='L4', max_length=30),
        ),
    ]
