from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from crudapp.models import TopicModel, PostModel, EmailForm, AnnonymousForm, BlogModel, InfoModel
from fileuploader.models import FileModel
from django.contrib.auth.models import User
from django.db.models import Count, Max, Sum
from django import forms
from crudapp.forms import TopicForm, PostForm, BlogForm
from django.utils import timezone
from datetime import date, timedelta
# from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.templatetags import fileuploader.fileuploader_tags
# from fileuploader import fileuploader_tags

def forum(request, string):
    print string
    # test = PostModel.objects.filter(author="art")
    # postModel = list(PostModel.objects.raw('SELECT * , max(pub_date), count(topic_id) AS freq, count(DISTINCT author) AS contributors FROM crudapp_postmodel GROUP BY topic_id ORDER BY pub_date DESC'))
    postModel = PostModel.objects.values('topic_id').annotate(freq=Count('author'), max=Max('pub_date'), contributors=Count('post'))
    # postModel = list(PostModel.objects.values('topic_id').annotate(freq=Count('topic_id'), contributors=Count('author', distinct=True)))
    paginator = Paginator(postModel, 20)
    page = request.GET.get('forum')
    try:
        forum_model = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        forum_model = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        forum_model = paginator.page(paginator.num_pages)


    # totalposts = PostModel.objects.annotate(Count('post'))
    # totalusers = User.objects.annotate(Count('id'))
    # totalfiles = FileModel.objects.filter(approved=True).annotate(Count('upload'))
    # totalarticles = BlogModel.objects.filter(approved=True).annotate(Count('article'))
    # totalviews = TopicModel.objects.aggregate(numviews = Sum('views'))
    # If there are topis with no posts the number of topics below will still be correct
    # totaltopics = PostModel.objects.aggregate(numtopics = Count('topic__id', distinct=True))
    context = {'forum_model': forum_model, 'current_time': timezone.now()}
    return render(request, 'forum_by_category.html', context)


def init(request):
    postModel = list(PostModel.objects.raw('SELECT *, max(pub_date), count(topic_id) AS freq, count(DISTINCT author) AS contributors FROM crudapp_postmodel GROUP BY topic_id ORDER BY pub_date DESC'))
    paginator = Paginator(postModel, 30)
    page2 = request.GET.get('forum')
    try:
        forum_model = paginator.page(page2)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        forum_model = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        forum_model = paginator.page(paginator.num_pages)

    blogModel = BlogModel.objects.all().order_by('pub_date').reverse()
    paginator = Paginator(blogModel, 5)
    page = request.GET.get('blog')
    try:
        blog_model = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blog_model = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blog_model = paginator.page(paginator.num_pages)
    # context = {'blog_model': blog_model}

    filemodel = FileModel.objects.all().reverse()
    paginator = Paginator(filemodel, 20)
    page = request.GET.get('file')
    try:
        file_model = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        file_model = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        file_model = paginator.page(paginator.num_pages)

    totalposts = PostModel.objects.annotate(Count('post'))
    totalusers = User.objects.annotate(Count('id'))
    totalfiles = FileModel.objects.filter(approved=True).annotate(Count('upload'))
    totalarticles = BlogModel.objects.filter(approved=True).annotate(Count('article'))
    totalviews = TopicModel.objects.aggregate(numviews = Sum('views'))
    # If there are topis with no posts the number of topics below will still be correct
    totaltopics = PostModel.objects.aggregate(numtopics = Count('topic__id', distinct=True))
    context = {'file_model': file_model, 'blog_model': blog_model, 'forum_model': forum_model, 'current_time':   timezone.now(), 'totalarticles': totalarticles, 'totalfiles': totalfiles, 'totalposts': totalposts, 'totaltopics': totaltopics, 'totalusers': totalusers, 'totalviews': totalviews}
    return render(request, 'forum.html', context)


def info(request):
    # if request.method == "POST":
    #     # userInstance = get_object_or_404(User, username = request.user)
    #     # using .get() because each user has a unique record
    #     userInstance = User.objects.get(username = request.user)
    #     Iform = InfoForm(   request.POST)
    #     if Iform.is_valid():
    #         iform = Iform.save(commit=False)
    #         iform.name = userInstance #this needs to be a user instance
    #         iform.user = request.user
    #         iform.save() #returns request and ids
    #         return redirect('info')
    # else:
    # info_model = InfoModel.objects.all()
    # info_model = InfoModel.objects.all().order_by('date')
    # info_model = InfoModel.objects.values('topicid')
    # info_model = InfoModel.objects.values('topicid').annotate(freq=Count('postid'))
    # info_model = InfoModel.objects.values('topicid').annotate( max=Max('date'), freq=Count('postid'), contributors=Count('author', distinct=True))#same result as line below
    # info_model = InfoModel.objects.values('topicid').annotate( max=Max('date')).annotate(freq=Count('postid')).annotate(contributors=Count('author', distinct=True))
    # info_model = InfoModel.objects.values('topicid').annotate( max=Max('date')).annotate(freq=Count('postid')).annotate(contributors=Count('author', distinct=True)).order_by('date')
    # info_model = InfoModel.objects.values('topicid').annotate( max=Max('date'), freq=Count('postid'), contributors=Count('author', distinct=True)).order_by('-date')
    info_model = InfoModel.objects.values('topicid').annotate( max=Max('date'), freq=Count('postid'), contributors=Count('author', distinct=True))


    paginator = Paginator(info_model, 20)
    page = request.GET.get('page')
    try:
        info = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        info = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        info = paginator.page(paginator.num_pages)
    return render(request, 'info.html', {'info': info})


def blog_form(request):
    if request.method == "POST":
        userInstance = User.objects.get(username = request.user)
        Bform = BlogForm(request.POST)
        if Bform.is_valid():
            bform = Bform.save(commit=False)
            bform.author = userInstance
            bform.pub_date = timezone.now()
            bform.submitted_date = timezone.now()
            bform.approved = False
            bform.save()
            # email admin
            admin_email = User.objects.all().filter(is_superuser = True)
            subject = 'Article submitted to QQIresources, awaiting approval'
            to_email = admin_email[0].email
            from_email = request.user.email
            message = '\n An article has been submitted to QQIresources by ' + str(request.user) + ' and is awaiting admin approval. \n'
            message += '\n Title: ' + str(bform.title) + '\n'
            message += '\n Author: ' + str(bform.author) + '\n'
            message += '\n Article: ' + str(bform.article) + '\n'
            message += '\n http://localhost:8000/admin' + '\n'
            send_mail(subject, message, from_email, [to_email])
            return redirect('init')
    else:
        blogform = BlogForm()
    return render(request, 'blog_form.html', {'blogform': blogform})

def report(request, id):
    reports = PostModel.objects.get(pk = id)
    admin_email = User.objects.all().filter(is_superuser = True)
    subject = 'A QQIresources post has been reported by ' + str(request.user)
    to_email = admin_email[0].email
    from_email = request.user.email
    message = '\n Post author: ' + reports.author + '\n'
    message += '\n Thread: ' + str(reports.topic.topic) + '\n'
    message += '\n Post: ' + str(reports.post) + '\n'
    message += '\n url: http://localhost:8000/thread/' + str(reports.topic_id) + '\n'
    message += '\n Reported by ' + str(request.user) + '\n'
    message += '\n' + str(request.user) + ' can be contacted at ' + str(request.user.email) + '\n'
    message += '\n Edit or delete this at http://localhost:8000/admin'
    send_mail(subject, message, from_email, [to_email])
    return HttpResponse('', content_type="text/plain")

def vote_up(request, id):
    posts = PostModel.objects.get(pk = id)
    posts.vote += 1
    PostModel.objects.filter(pk=id).update(vote=posts.vote)
    return HttpResponse(posts.vote, content_type="text/plain")

def vote_down(request, id):
    posts = PostModel.objects.get(pk = id)
    posts.vote -= 1
    PostModel.objects.filter(pk=id).update(vote=posts.vote)
    return HttpResponse(posts.vote, content_type="text/plain")

def vote_up_article(request, id):
    posts = BlogModel.objects.get(pk = id)
    posts.vote += 1
    BlogModel.objects.filter(pk=id).update(vote=posts.vote)
    return HttpResponse(posts.vote, content_type="text/plain")

def vote_down_article(request, id):
    posts = BlogModel.objects.get(pk = id)
    posts.vote -= 1
    BlogModel.objects.filter(pk=id).update(vote=posts.vote)
    return HttpResponse(posts.vote, content_type="text/plain")


def blog(request):
    blogModel_general_help = BlogModel.objects.filter(categories='General Help').filter(approved=True).order_by('pub_date').reverse()
    blogModel_sub_port = BlogModel.objects.filter(categories='Submitting Portfolios').filter(approved=True).order_by('pub_date').reverse()
    blogModel_gen_teach = BlogModel.objects.filter(categories='General Teaching').filter(approved=True).order_by('pub_date').reverse()
    blogModel_level12 = BlogModel.objects.filter(categories='Level 1 & 2').filter(approved=True).order_by('pub_date').reverse()
    blogModel_level3 = BlogModel.objects.filter(categories='Level 3').filter(approved=True).order_by('pub_date').reverse()
    blogModel_level4 = BlogModel.objects.filter(categories='Level 4').filter(approved=True).order_by('pub_date').reverse()
    blogModel_level5 = BlogModel.objects.filter(categories='Level 5').filter(approved=True).order_by('pub_date').reverse()
    blogModel_level6 = BlogModel.objects.filter(categories='Level 6').filter(approved=True).order_by('pub_date').reverse()

    paginator = Paginator(blogModel_general_help, 6)
    page = request.GET.get('blog_general_help')
    try:
        blog_model_general_help = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blog_model_general_help = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blog_model_general_help = paginator.page(paginator.num_pages)


    paginator = Paginator(blogModel_sub_port, 6)
    page = request.GET.get('blog_sub_port')
    try:
        blog_model_sub_port = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blog_model_sub_port = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blog_model_sub_port = paginator.page(paginator.num_pages)

    paginator = Paginator(blogModel_gen_teach, 6)
    page = request.GET.get('blog_gen_teach')
    try:
        blog_model_gen_teach = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blog_model_gen_teach = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blog_model_gen_teach = paginator.page(paginator.num_pages)

    paginator = Paginator(blogModel_level12, 6)
    page = request.GET.get('blog_level12')
    try:
        blog_model_level12 = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blog_model_level12 = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blog_model_level12 = paginator.page(paginator.num_pages)

    paginator = Paginator(blogModel_level3, 6)
    page = request.GET.get('blog_level3')
    try:
        blog_model_level3 = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blog_model_level3 = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blog_model_level3 = paginator.page(paginator.num_pages)

    paginator = Paginator(blogModel_level4, 6)
    page = request.GET.get('blog_level4')
    try:
        blog_model_level4 = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blog_model_level4 = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blog_model_level4 = paginator.page(paginator.num_pages)

    paginator = Paginator(blogModel_level5, 6)
    page = request.GET.get('blog_level5')
    try:
        blog_model_level5 = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blog_model_level5 = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blog_model_level5 = paginator.page(paginator.num_pages)

    paginator = Paginator(blogModel_level6, 6)
    page = request.GET.get('blog_level6')
    try:
        blog_model_level6 = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blog_model_level6 = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blog_model_level6 = paginator.page(paginator.num_pages)

    context = {'blog_model_general_help': blog_model_general_help, 'blog_model_sub_port': blog_model_sub_port, 'blog_model_gen_teach': blog_model_gen_teach, 'blog_model_level12': blog_model_level12, 'blog_model_level3': blog_model_level3, 'blog_model_level4': blog_model_level4, 'blog_model_level5': blog_model_level5, 'blog_model_level6': blog_model_level6 }
    return render(request, 'blog.html', context)


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
        if form.is_valid():
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
    pModel = PostModel.objects.all().filter(author = profileof).order_by('pub_date').reverse()
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

    blogModel = BlogModel.objects.filter(author = profileof).filter(approved=True).order_by('pub_date').reverse()
    paginator = Paginator(blogModel, 4)
    page = request.GET.get('blog')
    try:
        blog_model = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blog_model = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blog_model = paginator.page(paginator.num_pages)

    filemodel = FileModel.objects.filter(author = profileof).filter(approved=True).reverse()
    paginator = Paginator(filemodel, 10)
    page = request.GET.get('file')
    try:
        file_model = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        file_model = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        file_model = paginator.page(paginator.num_pages)

    anumber = BlogModel.objects.filter(author = profileof).filter(approved=True).annotate(articlefreq = Count('article'))
    fnumber = FileModel.objects.filter(author = profileof).filter(approved=True).annotate(uploadfreq = Count('upload'))
    pnumber = PostModel.objects.filter(author = profileof).annotate(postfreq = Count('post'))
    tnumber = PostModel.objects.filter(author = profileof).values('topic_id').distinct().annotate(topicfreq = Count('topic_id'))
    return render(request, 'profile.html', {'file_model': file_model, 'blog_model': blog_model, 'profile_model': profile_model, 'current_time': timezone.now(), 'name': profileof, 'pnumber': pnumber, 'tnumber': tnumber, 'fnumber': fnumber, 'anumber': anumber})


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

    return render(request, 'site_users.html', {'users_model': users_model, 'current_time':   timezone.now()})

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
        pModel = PostModel.objects.all().filter(topic_id = pk).order_by('pub_date').reverse()
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
        print 'Error: topic_form is not validating input'
        return redirect('init')
    else:
        topicform = TopicForm()
        postform = PostForm()
    # topicform = TopicForm()
    # postform = PostForm()
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
