from django.shortcuts import render, get_object_or_404, redirect
from .models import TopicModel, PostModel, EmailForm, AnnonymousForm, BlogModel
from django.contrib.auth.models import User
from django.db.models import Count, Max, Sum
from django import forms
from .forms import TopicForm, PostForm, BlogForm
from django.utils import timezone
from datetime import date, timedelta
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def blog_form(request):
    if request.method == "POST":
        Bform = BlogForm(request.POST)
        if Bform.is_valid():
            bform = Bform.save(commit=False)
            bform.author = request.user
            bform.pub_date = timezone.now()
            bform.submitted_date = timezone.now()
            bform.approved = False
            bform.save()
            # email admin
            admin_email = User.objects.all().filter(is_superuser = True)
            subject = 'Article submitted to QQIresources, awaiting approval'
            to_email = admin_email[0].email
            from_email = request.user.email
            message = 'An article has been submitted to QQIresources by ' + str(request.user) + ' and is awaiting admin approval. \n \n Title: ' + str(bform.title) + '\n Author: ' + str(bform.author) + '\n Article: ' + str(bform.article)
            send_mail(subject, message, from_email, [to_email])
            return redirect('init')
    else:
        blogform = BlogForm()
    return render(request, 'blog_form.html', {'blogform': blogform})


def blog(request):
    blogModel = BlogModel.objects.all().order_by('pub_date').reverse()
    paginator = Paginator(blogModel, 6)
    page = request.GET.get('page')
    try:
        blog_model = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blog_model = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blog_model = paginator.page(paginator.num_pages)
    context = {'blog_model': blog_model}
    return render(request, 'blog.html', context)

# Create your views here.
def init(request):
    postModel = list(PostModel.objects.raw('SELECT *, max(pub_date), count(topic_id) AS freq FROM crudapp_postmodel GROUP BY topic_id ORDER BY pub_date DESC LIMIT 0,20'))
    paginator = Paginator(postModel, 10)
    page = request.GET.get('page')
    try:
        forum_model = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        forum_model = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        forum_model = paginator.page(paginator.num_pages)

    totalposts = PostModel.objects.annotate(Count('post'))
    totaltopics = TopicModel.objects.annotate(postfreq = Count('topic'))
    totalusers = User.objects.annotate(postfreq = Count('id'))
    totalviews = TopicModel.objects.aggregate(numviews = Sum('views'))
    context = {'forum_model': forum_model, 'current_time':   timezone.now(), 'totalposts': totalposts, 'totaltopics': totaltopics, 'totalusers': totalusers, 'totalviews': totalviews}
    return render(request, 'forum.html', context)

def profile_contact(request, id):
    user = User.objects.all().filter(pk = id)
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated():
                from_email = request.user.email
                # request.user is an object which needs to be converted to a string for use in send_mail()
                name = str(request.user)
            to_email = user[0].email
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            full_message = '\n Email from: ' + from_email + '\n \n Email to: ' + to_email + '\n \n Name: ' + name + '\n \n ' + message
            try:
              send_mail(subject, full_message, from_email, [to_email])
              return render(request, 'profile_contact_form.html',{'emailform': emailform})
            except:
              return redirect('init')
        else:
          return redirect('init')
    else:
        emailform = EmailForm()
        send_to = str(user[0].username)
    return render(request, 'profile_contact_form.html',{'emailform': emailform, 'send_to': send_to})


def contact(request):
    #use id if user logged in to find sendfrom email
    #otherwise sendfrom email is email from form
    #if using profile sendfrom is logged in user
    # and send to is profile email
    if request.method == 'POST':
        if request.user.is_authenticated():
            form = EmailForm(request.POST)
        else:
            form = AnnonymousForm(request.POST)
        print 'I am here'
        if form.is_valid():
            print 'I am not here'
            if request.user.is_authenticated():
                from_email = request.user.email
                # request.user is an object which needs to be converted to a string for use in send_mail()
                name = str(request.user)
            else:
                from_email = form.cleaned_data['email']
                name = form.cleaned_data['name']
            # for contact form, email is always sent to admin
            logged_in_users = User.objects.all().filter(is_superuser = True)
            to_email = logged_in_users[0].email
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            full_message = '\n Email from: ' + from_email + '\n \n Email to: ' + to_email + '\n \n Name: ' + name + '\n \n ' + message
            try:
              send_mail(subject, full_message, from_email, [to_email])
              return render(request, 'contact_form.html',{'emailform': emailform, 'annonymousform': annonymousform})
            except:
              return redirect('init')
        else:
          return redirect('init')
    else:
        emailform = EmailForm()
        annonymousform = AnnonymousForm()
    return render(request, 'contact_form.html',{'emailform': emailform, 'annonymousform': annonymousform})


# profile for each User
def profile(request, id):
    name = User.objects.all().filter(pk = id)
    profileof = name[0]
    pModel = PostModel.objects.all().filter(author = profileof).reverse()
    paginator = Paginator(pModel, 10)
    page = request.GET.get('page')
    try:
        profile_model = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        profile_model = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        profile_model = paginator.page(paginator.num_pages)

    pnumber = PostModel.objects.filter(author = profileof).annotate(postfreq = Count('post'))
    tnumber = PostModel.objects.filter(author = profileof).values('topic_id').distinct().annotate(topicfreq = Count('topic_id'))
    return render(request, 'profile.html', {'profile_model': profile_model, 'current_time': timezone.now(), 'name': profileof, 'pnumber': pnumber, 'tnumber': tnumber})


def site_users(request):
    site_users = User.objects.all().reverse()
    paginator = Paginator(site_users, 10)
    page = request.GET.get('page')
    try:
        users_model = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users_model = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        users_model = paginator.page(paginator.num_pages)

    return render(request, 'site_users.html', {'users_model': users_model})

#display thread of posts and form for next post
def thread(request, id):
    if request.method == "POST":
        pk = id
        userInstance = User.objects.get(username = request.user)
        tform = get_object_or_404(TopicModel, pk = id)
        Pform = PostForm(request.POST)
        if Pform.is_valid():
            tform.author = userInstance
            pform = Pform.save(commit=False)
            pform.topic = tform
            pform.author = request.user
            pform.user = userInstance
            pform.pub_date = timezone.now()
            pform.save()
            return redirect('thread', id)
    else:
        pk=id
        pModel = PostModel.objects.all().filter(topic_id = pk).reverse()
        paginator = Paginator(pModel, 10)
        page = request.GET.get('page')
        try:
            thread_model = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            thread_model = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            thread_model = paginator.page(paginator.num_pages)

        postform = PostForm()
        post = get_object_or_404(TopicModel, pk = id)
        post.views += 1
        post.save()
        threadTopic = reversed(TopicModel.objects.all().filter(id = pk))
        num = id
        # How many posts are there for this topic_id
        numtopicposts = PostModel.objects.all().filter(topic_id = pk).annotate(postfreq = Count('post'))
        numtopicusers = PostModel.objects.all().filter(topic_id = pk).values('author').distinct().annotate(authorfreq = Count('author'))
        context = {'thread_model': thread_model, 'postform' : postform, 'current_time': timezone.now(), 'threadTopic': threadTopic, 'numtopicposts': numtopicposts, 'numtopicusers': numtopicusers}
    return render(request, 'thread.html', context)


#form for topic and first post also used to edit posts
def topic_form(request):
    if request.method == "POST":
        # userInstance = get_object_or_404(User, username = request.user)
        # using .get() because each user has a unique record
        userInstance = User.objects.get(username = request.user)
        Tform = TopicForm(request.POST)
        Pform = PostForm(request.POST)
        if Tform.is_valid() and Pform.is_valid():
            tform = Tform.save(commit=False)
            tform.topicAuthor = request.user
            tform.author = userInstance #this needs to be a user instance
            tform.save() #returns request and id
            pform = Pform.save(commit=False)
            pform.topic = tform
            pform.user = userInstance
            pform.author = request.user
            pform.pub_date = timezone.now()
            pform.save()
            return redirect('init')
    else:
        topicform = TopicForm()
        postform = PostForm()
    return render(request, 'new_topic.html', {'topicform': topicform, 'postform': postform})

#edit a post
def edit(request, id):
    print id
    post = get_object_or_404(PostModel, pk=id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False) #don't save model just yet
            # post.author = request.user
            post.pub_date = timezone.now()
            post.save()
            post = get_object_or_404(PostModel, pk=id)
            id = post.topic_id
            return redirect('thread', id)
    else:
        postform = PostForm(instance=post)
    return render(request, 'new_topic.html', {'postform': postform})

def todo(request):
    return render(request, 'todo.html')

#delete a post, actually replaces post with a message
def delete(request, id):
    post = get_object_or_404(PostModel, pk=id)
    form = PostForm(instance=post)
    post.post = "This post has been removed by the author"
    post.save()
    #id is the post's id and is used to get the id of the topic
    #id to be sent needs to be the topicid_id
    id = post.topic_id
    return redirect('thread', id)
