from __future__ import unicode_literals
from django.db import models
from django import forms
from django.utils import timezone
from tinymce.models import HTMLField
#
# class Members(models.Model):
#     first_name = models.CharField(max_length=200)
#     last_name = models.CharField(max_length=200)
#     topic = models.CharField(max_length=100)
#     post = models.CharField(max_length=100)
#     pub_date = models.DateTimeField('date published')
#     author = models.CharField(max_length=30)
#     def __str__(self):
#         return ' '. join([ self.first_name, self.last_name, ])

class TopicModel(models.Model):
    topic = models.CharField(max_length=100)
    topicAuthor = models.CharField(max_length=100)
    # topic = HTMLField(blank=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):              # __unicode__ on Python 2
            return self.topic

class PostModel(models.Model):
    post = HTMLField(blank=True, max_length=1000)
    pub_date = models.DateTimeField('date published')
    author = models.CharField(max_length=30)
    topicid = models.ForeignKey(TopicModel, related_name = 'posts')
    # topicid = models.ForeignKey(TopicModel, on_delete=models.CASCADE, null=True)

    def __str__(self):              # __unicode__ on Python 2
            return self.post

# test models
# class Reporter(models.Model):
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     email = models.EmailField()
#
#     def __str__(self):              # __unicode__ on Python 2
#         return "%s %s" % (self.first_name, self.last_name)
#
# class Article(models.Model):
#     headline = models.CharField(max_length=100)
#     pub_date = models.DateField()
#     reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
#
#     def __str__(self):              # __unicode__ on Python 2
#         return self.headline
#
#     class Meta:
#         ordering = ('headline',)
