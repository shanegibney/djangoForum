from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.db import models
from .models import FileModel
from crudapp.models import NewUserModel
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
        #print request.user.id
        if file.is_valid():
            fform = file.save(commit=False)
            fform.author = request.user
            # fform.pub_date = timezone.now()
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
            message += '\n Submitted: ' + str(fform.submitted_date)
            message += '\n Title: ' + str(fform.title)
            # message += '\n Category: ' + str(fform.get_categories_display)
            # need long namefor category here instead of short name
            # may need to go into file model to get it
            message += '\n Category: ' + str(fform.categories)
            message += '\n Author: ' + str(fform.author)
            message += '\n Description: ' + str(fform.description)
            message += '\n File name: ' + str(fform.upload)
            message += '\n Approve this file at: http://localhost:8000/admin'
            send_mail(subject, message, from_email, [to_email])
            
            # email user to verify file has been submitted and is awaiting approval
            from_email = to_email
            to_email = request.user.email
            message = 'Hello ' + str(fform.author) + ',\n'
            message += '\n Thank you for submitting your file to http://www.QQIresources.com The file ' + str(fform.upload) + ' has been successfully submitted and is awaiting approval. You will receive an email when it is approved. \n'
            message += '\n Submitted: ' + str(fform.submitted_date)
            message += '\n Title: ' + str(fform.title)
            message += '\n Category: ' + str(fform.categories)
            message += '\n Description: ' + str(fform.description) + '\n'
            message += '\n If you feel your file(s) are not being approved quick enough (more than 3 days) or you do not receive an email like this one for each file that you submitted, please contact us at http://localhost:8000/profile_contact/6/ as this sounds like something has got lost in the system! \n'
            message += '\n We very much appreciate your contribution as it will no doubt be of great benefit to other tutors. Remember you can always delete your own files at anytime. But if you are having any difficulty with this contact us.\n'
            message += '\n Thank you again,\n'
            message += '\n Shane'
            send_mail(subject, message, from_email, [to_email])

            # add this user to NewUserModel,
            # only if they don't exist their,
            # so that their submission can be approved later
            try:
                obj = NewUserModel.objects.get(user_id=request.user.id)
            except NewUserModel.DoesNotExist:
                obj = NewUserModel(user_id=request.user.id)
                obj.save()
            
            return redirect('init')
        else:
            print 'Not valid'
    fileform = FileForm()
    context = {'fileform': fileform}
    # return render_to_response('file_form.html', context_instance=RequestContext(request, context))
    # return render_to_response('file_form.html', context=RequestContext(request, context))
    return render(request, 'file_form.html', context)

def vote_up_file(request, id):
    posts = FileModel.objects.get(pk = id)
    posts.vote += 1
    FileModel.objects.filter(pk=id).update(vote=posts.vote)
    return HttpResponse(posts.vote, content_xotype="text/plain")

def vote_down_file(request, id):
    posts = FileModel.objects.get(pk = id)
    posts.vote -= 1
    FileModel.objects.filter(pk=id).update(vote=posts.vote)
    return HttpResponse(posts.vote, content_type="text/plain")
