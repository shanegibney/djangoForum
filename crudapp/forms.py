# from django.db import models
from django import forms
from .models import TopicModel, PostModel, BlogModel
from tinymce.widgets import TinyMCE
from django.db import models


class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        fields = ('id', 'title', 'article')

class TopicForm(forms.ModelForm):
    class Meta:
        model = TopicModel
        fields = ('id', 'forum', 'topic')

class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        # post = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
        fields = ('id', 'post')
