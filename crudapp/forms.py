# from django.db import models
from django import forms
from .models import Members

# class NameForm(forms.Form):
#     your_name = forms.CharField(label='Your name', max_length=100)

class MemberForm(forms.ModelForm):
    # print 'this is the MemberForm'
    class Meta:
        model = Members
        # which fields to put in form
        fields = ('first_name', 'last_name', 'description')
