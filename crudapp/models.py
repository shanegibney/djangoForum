from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone
from tinymce.models import HTMLField
from django.db import models
from tinymce.widgets import TinyMCE

class InfoModel(models.Model):
    name = models.ForeignKey(User)
    user = models.CharField(max_length=30)
    vote = models.IntegerField(default=0)
    category1 = 'category 1'
    category2 = 'category 2'
    category3 = 'category 3'
    category4 = 'category 4'
    categories = (
        (category1, 'category 1'),
        (category2, 'category 2'),
        (category3, 'category 3'),
        (category4, 'category 4'),
    )
    category = models.CharField(
        max_length = 10,
        choices = categories,
        default = category4,
    )

class BlogModel(models.Model):
    title = models.CharField(max_length=100)
    article = models.CharField(max_length=255)
    pub_date = models.DateTimeField('date published')
    submitted_date = models.DateTimeField('date submitted')
    # author = models.CharField(max_length=255)
    # user = models.ForeignKey(User)
    author = models.ForeignKey(User)
    approved = models.BooleanField(default=False)
    vote = models.IntegerField(default=0)
    def __str__(self):              # __unicode__ on Python 2
            return 'approved, ' + str(self.approved) + ' article, ' + self.article

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
    level1 = 'L1'
    level2 = 'L2'
    level3 = 'L3'
    level4 = 'L4'
    YEAR_IN_SCHOOL_CHOICES = (
        (level1, 'Level 1'),
        (level2, 'Level 2'),
        (level3, 'Level 3'),
        (level4, 'Level 4'),
    )
    forum = models.CharField(
        max_length=2,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default=level4,
    )
    # topic = HTMLField(blank=True)
    #
    # def is_upperclass(self):
    #     return self.year_in_school in (self.JUNIOR, self.SENIOR)

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
