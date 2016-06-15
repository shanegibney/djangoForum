# from __future__ import unicode_literals
# from django.db import models
# from django.contrib.auth.models import User
# from django import forms
# from django.utils import timezone
# from tinymce.models import HTMLField
# from django.db import models


# class Members(models.Model):
#     first_name = models.CharField(max_length=200)
#     last_name = models.CharField(max_length=200)
#     topic = models.CharField(max_length=100)
#     post = models.CharField(max_length=100)
#     pub_date = models.DateTimeField('date published')
#     author = models.CharField(max_length=30)
#     def __str__(self):
#         return ' '. join([ self.first_name, self.last_name, ])


# class BlogModel(models.Model):
#     title = models.CharField(max_length=100)
#     article = models.CharField(max_length=255)
#     pub_date = models.DateTimeField('date published')
#     submitted_date = models.DateTimeField('date submitted')
#     author = models.CharField(max_length=255)
#     approved = models.BooleanField(default=False)
#     def __str__(self):              # __unicode__ on Python 2
#             return 'approved, ' + str(self.approved) + ' article, ' + self.article
#
# class AnnonymousForm(forms.Form):
#     name = forms.CharField(max_length=255)
#     email = forms.EmailField()
#     subject = forms.CharField(max_length=255)
#     message = forms.CharField(max_length=800)
#
# class EmailForm(forms.Form):
#     subject = forms.CharField(max_length=255)
#     message = forms.CharField(max_length=800)

# class TopicModel(models.Model):
#     topic = models.CharField(blank=False, max_length = 100)
#     topicAuthor = models.CharField(max_length = 100)
#     author = models.ForeignKey(User)
#     # topic = HTMLField(blank=True)
#     views = models.PositiveIntegerField(default = 0)
#
#     def __str__(self):              # __unicode__ on Python 2
#             return self.topic

# class PostModel(models.Model):
#     post = HTMLField(blank=False, max_length = 1000)
#     pub_date = models.DateTimeField('date published')
#     author = models.CharField(max_length = 30)
#     user =  models.ForeignKey(User)
#     topic = models.ForeignKey(TopicModel)
#     # topicid = models.ForeignKey(TopicModel, on_delete=models.CASCADE, null=True)
#
#     def __str__(self):              # __unicode__ on Python 2
#             return self.post

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
