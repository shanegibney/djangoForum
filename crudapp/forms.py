# from django.db import models
from django import forms
from .models import TopicModel, PostModel
from tinymce.widgets import TinyMCE


# class MemberForm(forms.ModelForm):
#     # print 'this is the MemberForm'
#     class Meta:
#         model = Members
#         # which fields to put in form
#         fields = ('topic', 'post')

class TopicForm(forms.ModelForm):
    class Meta:
        model = TopicModel
        fields = ('id', 'topic')

class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        # post = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
        fields = ('id', 'post',)
