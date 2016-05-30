from __future__ import unicode_literals
from django.db import models
# from django.contrib.auth.models import User
from django import forms
# from django.utils import timezone
# from tinymce.models import HTMLField


class FileModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    pub_date = models.DateTimeField('date published')
    submitted_date = models.DateTimeField('date submitted')
    author = models.CharField(max_length=255)
    approved = models.BooleanField(default=False)
    upload = models.FileField()
    def __str__(self):
            return self.title
