from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.db import models
from .models import FileModel
from django.contrib.auth.models import User
# from django.contrib.auth.models import User
# from django.db.models import Count, Max, Sum
from django import forms
from .forms import FileForm
from django.utils import timezone
# from datetime import date, timedelta
# from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
# from django.core.mail import send_mail, BadHeaderError


def file_sharing(request):
    filemodel = reversed(FileModel.objects.all())
    context = {'filemodel': filemodel}
    return render(request, 'upload.html', context)


# def upload_file(request):
#     if request.method == 'POST':
#         form = ModelFormWithFileField(request.POST, request.FILES)
#         if form.is_valid():
#             # file is saved
#             form.save()
#             return HttpResponseRedirect('/success/url/')
#     else:
#         form = ModelFormWithFileField()
#     return render(request, 'upload.html', {'form': form})

def file_sharing_form(request):
    if request.method == "POST":
        file = FileForm(request.POST, request.FILES)
        print 'i am outside of is valid'
        if file.is_valid():
            print 'is valid in here'
            fform = file.save(commit=False)
            # fform = FileModel(docfile = request.FILES['docfile'])
            fform.author = request.user
            fform.pub_date = timezone.now()
            fform.submitted_date = timezone.now()
            fform.approved = False
            fform.save()
            # email admin
            admin_email = User.objects.all().filter(is_superuser = True)
            subject = 'File submitted to QQIresources, awaiting approval'
            to_email = admin_email[0].email
            from_email = request.user.email
            message = 'A file has been submitted to QQIresources by ' + str(request.user) + ' and is awaiting admin approval. \n \n Title: ' + str(fform.title) + '\n Author: ' + str(fform.author) + '\n Description: ' + str(fform.description)
            send_mail(subject, message, from_email, [to_email])
            return redirect('init')
        else:
            print 'Not valid'
    fileform = FileForm()
    context = {'fileform': fileform}
    return render_to_response('file_form.html', context_instance=RequestContext(request, context))
