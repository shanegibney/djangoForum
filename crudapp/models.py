from __future__ import unicode_literals
from django.db import models
from django import forms
from django.utils import timezone

# Create your models here.

class Members(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    description = models.CharField(max_length=600)
    pub_date = models.DateTimeField('date published')
    author = models.CharField(max_length=30)
    def __str__(self):
        return ' '. join([ self.first_name, self.last_name, ])
