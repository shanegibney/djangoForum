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
    categories = (
        (category1, 'category 1'),
        (category2, 'category 2'),
    )
    category = models.CharField(
        max_length = 10,
        choices = categories,
        default = category2,
    )

class BlogModel(models.Model):
    title = models.CharField(max_length=100)
    article = models.CharField(max_length=255)
    pub_date = models.DateTimeField('date published')
    submitted_date = models.DateTimeField('date submitted')
    # author = models.CharField(max_length=255)
    # user = models.ForeignKey(User)
    forum_categories = (
        ('General Help', 'General Help'),
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
    # gh = 'General Help'
    # sp = 'Submitting Portfolios'
    # gt = 'General Teaching'
    # l12 = 'Level 1 & 2'
    # l3 = 'Level 3'
    # l4 = 'Level 4'
    # l5 = 'Level 5'
    # l6 = 'Level 6'
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

# SHIRT_SIZES = (
#         ('S', 'Small'),
#         ('M', 'Medium'),
#         ('L', 'Large'),
#     )
#     name = models.CharField(max_length=60)
#     shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)
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
