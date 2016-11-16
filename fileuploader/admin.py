from django.contrib import admin
from .models import FileModel
from django.contrib.auth.models import User
from .forms import FileForm
from crudapp.models import NewUserModel
#from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.core.mail import send_mail, BadHeaderError
from django.core.exceptions import PermissionDenied
from django.contrib import admin
from django.contrib.admin.actions import delete_selected as delete_selected_

# see https://gist.github.com/rudyryk/4190318
# overrides and recreates delete_selected
def delete_selected(modeladmin, request, queryset):
    if not modeladmin.has_delete_permission(request):
        raise PermissionDenied
    if request.POST.get('post'):
        for obj in queryset:
            obj.delete()
    else:
        return delete_selected_(modeladmin, request, queryset)
delete_selected.short_description = "Delete selected objects"

class FileModelAdmin(admin.ModelAdmin):
    form = FileForm
    fields = ('title', 'description', 'categories', 'pub_date', 'submitted_date', 'author', 'user', 'approved', 'upload', 'vote')
    # pass
    list_display = ['title', 'approved', 'author', 'user', 'categories', 'description', 'pub_date', 'submitted_date', 'upload', 'vote']
    actions = ['approve_files', 'delete_selected']

    # 'Approve files' action, act on  multiple checks files simultaneously
    def approve_files(self, request, qs):
        for obj in qs:
            # author = qs.author
            user = obj.user
            adminApproved = obj.approved # approved status on admin site
            userInstance = User.objects.get(username=user)
            id = obj.id
            item = FileModel.objects.get(pk=id)
            item.pub_date = timezone.now()
            item.save()

            file_name = str(item.upload)
            description = item.description
            title = item.title
            categories = item.categories
            submitted = str(item.submitted_date)
            published = str(item.pub_date)
            
            approved = item.approved # approved status in FileModel
            id = userInstance.id
            item = NewUserModel.objects.get(user_id=id)
            if(approved == False):
                item.files += 1

                # email user that their file has been approved
                admin_email = User.objects.all().filter(is_superuser=True)
                subject = 'QQIresource file approved'
                from_email = admin_email[0].email
                to_email = userInstance.email
                print "from_email %s" %(from_email)
                print "to_email %s" %(to_email)
                message = 'Hello %s \n' %(user)
                message +=  '\n Thank you for submitting your file to http://www.QQIresources.com This file has been approved and is now being shared with other tutors. \n'
                message += '\n File name: ' + file_name
                message += '\n Title: ' + title
                message += '\n Category: ' + categories
                message += '\n Description: ' + description
                message += '\n Submitted: ' + submitted
                message += '\n Published ' + published +'\n'
                message += '\n You can always delete this file yourself at any time, contact us if you are having any difficulty with this. \n'
                message += '\n Your submission is greatly appreciated. \n'
                message += '\n Thank you again and best regards, \n'
                message += '\n Shane \n'
                send_mail(subject, message, from_email, [to_email])
                
            item.save()
        obj.update(approved = True)
    # Also need to check how this behaves for a user that
    # that isn't in the usermodel yet, if user hasn't submitted a file
    
    # Save an object after editing, can only do one at a time
    def save_model(self, request, obj, form, change):
        user = obj.user
        print 'user: %s' %(user)
        u = User.objects.get(username=user)

        # add this user to NewUserModel,
        # only if they don't exist their,
        # so that their submission can be approved later
        try:
            obj = NewUserModel.objects.get(user_id=request.user.id)
        except NewUserModel.DoesNotExist:
            obj = NewUserModel(user_id=request.user.id)
            obj.save()


            
        # this 'try' block of code used when a FileModel instance already exists
        id = obj.id
        # print 'obj id: %d' %(id)
        item = FileModel.objects.get(pk=id)

        
        
        item.pub_date = timezone.now()
        item.save()
        # this model needs to be updated so that the published date is now
        file_name = str(item.upload)
        description = item.description
        title = item.title
        categories = item.categories
        submitted = str(item.submitted_date)
        published = str(item.pub_date)

        print "obj.approved %s --- status in admin site" %(obj.approved)
        print "item.approved %s --- status in FileModel" %(item.approved)
        if(item.approved != obj.approved):
            userInstance = User.objects.get(username=user)
            id = userInstance.id
            print "Am I ever here?"
            # In the case where a new file object is created by admin
            # it MAY be that this user is not in NewUserModel
            # need to fix this issue
            item = NewUserModel.objects.get(user_id=id)
            if(obj.approved == True):
                item.files += 1
                item.pub_date = timezone.now()
                item.save()
                admin_email = User.objects.all().filter(is_superuser=True)
                subject = 'QQIresource file approved'
                from_email = admin_email[0].email
                to_email = userInstance.email
                print "from_email %s" %(from_email)
                print "to_email %s" %(to_email)
                message = 'Hello %s \n' %(user)
                message +=  '\n Thank you for submitting your file to http://www.QQIresources.com This file has been approved and is now being shared with other tutors. \n'
                message += '\n File name: ' + file_name
                message += '\n Title: ' + title
                message += '\n Category: ' + categories
                message += '\n Description: ' + description
                message += '\n Submitted: ' + submitted
                message += '\n Published ' + published +'\n'
                message += '\n You can always delete this file yourself at any time, contact us if you are having any difficulty with this. \n'
                message += '\n Your submission is greatly appreciated. \n'
                message += '\n Thank you again and best regards, \n'
                message += '\n Shane \n'
                send_mail(subject, message, from_email, [to_email])
            else:
                item.files -= 1
                item.save()
        obj.save() # Saving again may be an issue

            # print "You are an admin trying to create a new FileModel instance"
            # A new NewUserModel instance needs to be created if this user doesn't exist
            # normally this would be created when user submits a file
            # but here user does not submit file, it is created by admin
            # approve file
            # item.file += 1
            # 

            
    # Delete an object after editing, can only do one at a time
    def delete_model(self, request, queryset):
        # author = queryset.author
        user = queryset.user
        userInstance = User.objects.get(username=user)
        id = queryset.id
        item = FileModel.objects.get(pk=id)
        approved = item.approved # approved status in FileModel
        #filename=obj.profile_name+".xml"
        #os.remove(os.path.join(obj.type,filename))
        id = userInstance.id
        item = NewUserModel.objects.get(user_id=id)
        # -1 for file in filemodel only if approved
        if approved == True:
            item.files -= 1
            item.save()
        queryset.delete()

    # The 'Delete selected' action, acts on multiple checked objects
    def delete_selected(self, request, queryset):
        for obj in queryset:
            # author = obj.author
            user = obj.user
            adminApproved = obj.approved # approved status on admin site
            userInstance = User.objects.get(username=user)
            id = obj.id
            item = FileModel.objects.get(pk=id)
            approved = item.approved # approved status in FileModel
            id = userInstance.id
            item = NewUserModel.objects.get(user_id=id)
            # For the case where a file is deleted but was approved yet
            if approved == True:
                item.files -= 1
                item.save()
        queryset.delete()
        
admin.site.register(FileModel, FileModelAdmin)
