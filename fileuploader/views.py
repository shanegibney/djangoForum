from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.db import models
from .models import FileModel
from django.contrib.auth.models import User
from django import forms
from .forms import FileForm
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def file_sharing(request):
    filemodel = FileModel.objects.all().reverse()
    paginator = Paginator(filemodel, 2)
    page = request.GET.get('page')
    try:
        file_model = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        file_model = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        file_model = paginator.page(paginator.num_pages)

    context = {'file_model': file_model}
    return render(request, 'upload.html', context)


def file_sharing_form(request):
    if request.method == "POST":
        file = FileForm(request.POST, request.FILES)
        print 'i am outside of is valid'
        if file.is_valid():
            print 'is valid in here'
            fform = file.save(commit=False)
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
