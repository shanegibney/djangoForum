# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-19 23:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crudapp', '0037_auto_20160619_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topicmodel',
            name='categories',
            field=models.CharField(choices=[('GeneralHelp', 'General Help'), ('Submitting Portfolios', 'SubmittingPortfolios'), ('General Teaching', 'General Teaching'), ('Level 1 & 2', 'Level 1 & 2'), ('Level 3', 'Level 3'), ('Level 4', 'Level 4'), ('Level 5', 'Level 5'), ('Level 6', 'Level 6')], default='Level 4', max_length=30),
        ),
    ]