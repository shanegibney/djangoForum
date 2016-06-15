from django.db import models
from django import forms
from .models import FileModel
# from tinymce.widgets import TinyMCE
from django.utils import timezone


class FileForm(forms.ModelForm):
    class Meta:
        model = FileModel
        # fields = '__all__'
        fields = ('id', 'categories', 'title', 'description', 'upload')

    def save(self, force_insert=False, force_update=False, commit=True):
        m = super(FileForm, self).save(commit=False)
        # do custom stuff
        m.pub_date = timezone.now()
        if commit:
            m.save()
        return m
