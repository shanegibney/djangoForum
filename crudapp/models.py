from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone
from tinymce.models import HTMLField
from django.db import models
from tinymce.widgets import TinyMCE

class NewUserModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    posts = models.IntegerField(default=0)
    articles = models.IntegerField(default=0)
    files = models.IntegerField(default=0)

class TempModel(models.Model):
    topicid = models.IntegerField(default=0)
    date = models.DateTimeField('date published')
    author = models.CharField(max_length=30)

class InfoModel(models.Model):
    topicid = models.IntegerField(default=0)
    postid = models.IntegerField(default=0)
    author = models.CharField(max_length=30)
    post = models.CharField(max_length=30)
    date = models.DateTimeField('date published')

class BlogModel(models.Model):
    title = models.CharField(max_length=100)
    article = models.CharField(max_length=255)
    pub_date = models.DateTimeField('date published')
    submitted_date = models.DateTimeField('date submitted')
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
    author = models.ForeignKey(User)
    approved = models.BooleanField(default=False)
    vote = models.IntegerField(default=0)
    def __str__(self):              # __unicode__ on Python 2
            return 'Approved, ' + str(self.approved) + ' Article, ' + self.article

class AnnonymousForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    subject = forms.CharField(max_length=255)
    message = forms.CharField(max_length=800)

class EmailForm(forms.Form):
    subject = forms.CharField(max_length=255)
    message = forms.CharField(max_length=800)

class TopicModel(models.Model):
    topic = models.CharField(max_length = 100)
    topicAuthor = models.CharField(max_length = 100)
    author = models.ForeignKey(User)
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

    views = models.PositiveIntegerField(default = 0)
    def __str__(self):              # __unicode__ on Python 2
            return self.topic

class PostModel(models.Model):
    post = HTMLField(blank = True, max_length = 1000)
    # post = models.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    pub_date = models.DateTimeField('date published')
    author = models.CharField(max_length = 30)
    user =  models.ForeignKey(User)
    topic = models.ForeignKey(TopicModel)
    vote = models.IntegerField(default=0)

    def __str__(self):              # __unicode__ on Python 2
            return self.post
