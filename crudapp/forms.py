# from django.db import models
from django import forms
from .models import TopicModel, PostModel, BlogModel, InfoModel
from tinymce.widgets import TinyMCE
from django.db import models
from django.utils import timezone

# Blog is the articles section of the project
class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        # fields = '__all__'
        fields = ('id', 'categories', 'title', 'article')

    def save(self, force_insert=False, force_update=False, commit=True):
        m = super(BlogForm, self).save(commit=False)
        # do custom stuff
        m.pub_date = timezone.now()
        if commit:
            m.save()
        return m

# class BlogForm(forms.ModelForm):
#     class Meta:
#         model = BlogModel
#         fields = ('id', 'title', 'article')

# class InfoForm(forms.ModelForm):
#     class Meta:
#         model = InfoModel
#         fields = ('id', 'vote', 'category')

class TopicForm(forms.ModelForm):
    class Meta:
        model = TopicModel
        fields = ('id', 'categories', 'topic')

class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        # post = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
        fields = ('id', 'post')
