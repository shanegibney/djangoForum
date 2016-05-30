from django.db import models
from django import forms
from .models import FileModel
# from tinymce.widgets import TinyMCE

class FileForm(forms.ModelForm):
    class Meta:
        model = FileModel
        fields = ('id', 'title', 'description', 'upload')
