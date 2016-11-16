from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django import forms
# from django.utils import timezone
# from tinymce.models import HTMLField

class FileModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    pub_date = models.DateTimeField('date published', blank=True)
    # pub_date = models.DateTimeField('date published')
    submitted_date = models.DateTimeField('date submitted')
    author = models.CharField(max_length=255)
    user =  models.ForeignKey(User, default=6)
    approved = models.BooleanField(default=False)
    upload = models.FileField()
    GeneralHelp = 'GH'
    SubmittingPortfolios = 'SP'
    GeneralTeaching = 'GT'
    Level12 = 'L12'
    Level3 = 'L3'
    Level4 = 'L4'
    Level5 = 'L5'
    Level6 = 'L6'
    forum_categories = (
        (GeneralHelp, 'General Help'),
        (SubmittingPortfolios, 'Submitting Portfolios'),
        (GeneralTeaching, 'General Teaching'),
        (Level12, 'Level 1 & 2'),
        (Level3, 'Level 3'),
        (Level4, 'Level 4'),
        (Level5, 'Level 5'),
        (Level6, 'Level 6'),
    )
    categories = models.CharField(
        max_length=30,
        choices=forum_categories,
        default=Level4,
    )
    vote = models.IntegerField(default=0)
    def __str__(self):              # __unicode__ on Python 2
            return 'Approved, ' + str(self.approved) + ' Title, ' + self.title
