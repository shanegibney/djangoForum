from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django import forms
# from django.utils import timezone
# from tinymce.models import HTMLField


class FileModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    pub_date = models.DateTimeField('date published')
    submitted_date = models.DateTimeField('date submitted')
    author = models.CharField(max_length=255)
    user =  models.ForeignKey(User, default=6)
    approved = models.BooleanField(default=False)
    upload = models.FileField()
    forum_categories = (
        ('general Help', 'General Help'),
        ('Submitting Portfolios', 'Submitting Portfolios'),
        ('General Teaching', 'General Teaching'),
        ('Level 1 & 2', 'Level 1 & 2'),
        ('Level 3', 'Level 3'),
        ('Level 4', 'Level 4'),
        ('Level 5', 'Level 5'),
        ('Level 6', 'Level 6'),
    )
    categories = models.CharField(
        max_length=21,
        choices=forum_categories,
        default='Level 4',
    )
    vote = models.IntegerField(default=0)
    def __str__(self):              # __unicode__ on Python 2
            return 'Approved, ' + str(self.approved) + ' Title, ' + self.title
