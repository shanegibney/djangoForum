from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.db import models
from .models import FileModel
from django.contrib.auth.models import User
from django import forms
from .forms import FileForm
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def file_sharing(request, categ):
    if categ == 'all':
        filemodel = FileModel.objects.all().reverse()
    else:
        filemodel = FileModel.objects.filter(categories=categ).reverse()

    paginator = Paginator(filemodel, 10)
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
        userInstance = User.objects.get(username = request.user)
        if file.is_valid():
            fform = file.save(commit=False)
            fform.author = request.user
            fform.pub_date = timezone.now()
            fform.submitted_date = timezone.now()
            fform.user = userInstance
            fform.approved = False
            fform.save()
            # email admin
            admin_email = User.objects.all().filter(is_superuser = True)
            subject = 'File submitted to QQIresources, awaiting approval'
            to_email = admin_email[0].email
            from_email = request.user.email
            message = 'A file has been submitted to QQIresources by ' + str(request.user) + ' and is awaiting admin approval. \n '
            message += '\n Title: ' + str(fform.title) + '\n'
            message += '\n Author: ' + str(fform.author) + '\n'
            message += '\n Description: ' + str(fform.description) + '\n'
            message += '\n http://localhost:8000/admin'
            send_mail(subject, message, from_email, [to_email])
            return redirect('init')
        else:
            print 'Not valid'
    fileform = FileForm()
    context = {'fileform': fileform}
    return render_to_response('file_form.html', context_instance=RequestContext(request, context))

def vote_up_file(request, id):
    posts = FileModel.objects.get(pk = id)
    posts.vote += 1
    FileModel.objects.filter(pk=id).update(vote=posts.vote)
    return HttpResponse(posts.vote, content_type="text/plain")

def vote_down_file(request, id):
    posts = FileModel.objects.get(pk = id)
    posts.vote -= 1
    FileModel.objects.filter(pk=id).update(vote=posts.vote)
    return HttpResponse(posts.vote, content_type="text/plain")
