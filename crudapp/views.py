from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from crudapp.models import TopicModel, PostModel, EmailForm, AnnonymousForm, BlogModel, InfoModel, TempModel, NewUserModel
from fileuploader.models import FileModel
from django.contrib.auth.models import User
from django.db.models import Count, Max, Sum, F
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

def temp(request):
    info2 = TempModel.objects.all()
    info = TempModel.objects.values('topicid').annotate( max=Max('date')).order_by('-max')

    columnlist = []
    for item in info2:
         columnlist.append([item])

    for item in info:
        for i in range(len(columnlist)):
            if item['max'] == columnlist[i][0].date:
                item['author'] = columnlist[i][0].author

    return render(request, 'template.html', {'info': info, 'info2': info2})

    
def forum(request, categ):
    postModelAll = PostModel.objects.all()
    if categ == 'all':
        postModel = PostModel.objects.all().values('topic_id').annotate( max=Max('pub_date'), freq=Count('topic_id'), contributors=Count('author', distinct=True)).order_by('-max')
    else:
        postModel = PostModel.objects.filter(topic__categories = categ).values('topic_id').annotate( max=Max('pub_date'), freq=Count('topic_id'), contributors=Count('author', distinct=True)).order_by('-max')

    columnlist = []
    for item in postModelAll:
         columnlist.append([item])

    # this foreignkey stuff could probably be done more efficiently using an instance
    for item in postModel:
        for i in range(len(columnlist)):
            if item['max'] == columnlist[i][0].pub_date:
                item['topic'] = columnlist[i][0].topic
                item['post'] = columnlist[i][0].post

    # level = postModel.topic.get_categories_.diplay()

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
    if categ == 'all':
        totalposts = PostModel.objects.all().annotate(Count('post'))
        # totalusers = TopicModel.objects.filter(categories = categ).values('author_id').annotate(Count('author_id', distinct=True))
        totalusers = TopicModel.objects.all().annotate(Count('author_id', distinct=True))
        # totalusers = TopicModel.objects.filter(categories = categ).aggregate(numusers = Sum('author', distinct=True))
        totalviews = TopicModel.objects.all().aggregate(numviews = Sum('views'))
    else:
        totalposts = PostModel.objects.filter(topic__categories=categ).annotate(Count('post'))
        # totalusers = TopicModel.objects.filter(categories = categ).values('author_id').annotate(Count('author_id', distinct=True))
        totalusers = TopicModel.objects.filter(categories = categ).annotate(Count('author_id', distinct=True))
        # totalusers = TopicModel.objects.filter(categories = categ).aggregate(numusers = Sum('author', distinct=True))
        totalviews = TopicModel.objects.filter(categories = categ).aggregate(numviews = Sum('views'))

    # If there are topics with no posts the number of topics below will still be correct
    # totaltopics = PostModel.objects.aggregate(numtopics = Count('topic__id', distinct=True))
    context = {'forum_model': forum_model, 'totalposts': totalposts, 'totalusers': totalusers, 'totalviews': totalviews, 'current_time': timezone.now()}
    return render(request, 'forum_by_category.html', context)


def init(request):
    # postModel = list(PostModel.objects.raw('SELECT *, max(pub_date), count(topic_id) AS freq, count(DISTINCT author) AS contributors FROM crudapp_postmodel GROUP BY topic_id ORDER BY pub_date DESC'))
    postModelAll = PostModel.objects.all()
    postModel = PostModel.objects.values('topic_id').annotate( max=Max('pub_date'), freq=Count('topic_id'), contributors=Count('author', distinct=True)).order_by('-max')

    columnlist = []
    for item in postModelAll:
         columnlist.append([item])

    # this foreignkey stuff could probably be done more efficiently using an instance
    for item in postModel:
        for i in range(len(columnlist)):
            if item['max'] == columnlist[i][0].pub_date:
                item['topic'] = columnlist[i][0].topic
                item['post'] = columnlist[i][0].post

    paginator = Paginator(postModel, 10)
    page2 = request.GET.get('forum')
    try:
        forum_model = paginator.page(page2)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        forum_model = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        forum_model = paginator.page(paginator.num_pages)

    totalposts = PostModel.objects.annotate(Count('post'))
    totalusers = User.objects.annotate(Count('id'))
    totalfiles = FileModel.objects.filter(approved=True).annotate(Count('upload'))
    totalarticles = BlogModel.objects.filter(approved=True).annotate(Count('article'))
    totalviews = TopicModel.objects.aggregate(numviews = Sum('views'))
    # If there are topis with no posts the number of topics below will still be correct
    totaltopics = PostModel.objects.aggregate(numtopics = Count('topic__id', distinct=True))
    context = {'forum_model': forum_model, 'current_time':  timezone.now(), 'totalarticles': totalarticles, 'totalfiles': totalfiles, 'totalposts': totalposts, 'totaltopics': totaltopics, 'totalusers': totalusers, 'totalviews': totalviews}
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
    # info_model = InfoModel.objects.values('topicid').annotate( max=Max('date'), freq=Count('postid'), contributors=Count('author', distinct=True))
    # info_model = InfoModel.objects.values('topicid').annotate( max=Max('date'), freq=Count('postid'), contributors=Count('author', distinct=True)).order_by('-max').filter(post='max')
    # info_model = InfoModel.objects.values('topicid').annotate( max=Max('date'), freq=Count('postid'), contributors=Count('author', distinct=True)).order_by('-max').all()
    # info_model = InfoModel.objects.values('topicid').annotate( max=Max('date'), freq=Count('postid'), contributors=Count('author', distinct=True)).order_by('-max').filter(topicid=2)
    # info_model = InfoModel.objects.values('topicid').annotate( max=Max('date'), freq=Count('postid'), contributors=Count('author', distinct=True)).order_by('-max')
    # info_model = InfoModel.objects.all().values('topicid').annotate( max=Max('date'), freq=Count('postid'), contributors=Count('author', distinct=True)).order_by('-max').filter(author__date='max')
    # info_model = InfoModel.objects.all().values('topicid').annotate( max=Max('date'), freq=Count('postid'), contributors=Count('author', distinct=True)).order_by('-max').filter(date=F('max'))
    # info_model = InfoModel.objects.all().values('topicid').annotate( max=Max('date'), freq=Count('postid'), contributors=Count('author', distinct=True)).order_by('-max').filter('post').get(date='max')
    # info_model = InfoModel.objects.all().values('topicid').annotate( max=Max('date'), freq=Count('postid'), contributors=Count('author', distinct=True)).order_by('-max')
    # info_model = InfoModel.objects.all().values('topicid').annotate( max=Max('date'), freq=Count('postid'), contributors=Count('author', distinct=True)).order_by('-max').filter(post='post')
    # info_model = InfoModel.objects.all().values('topicid').annotate( max=Max('date'), freq=Count('postid'), contributors=Count('author', distinct=True)).order_by('-max').values('post','author')
    # info_model = InfoModel.objects.all().values('topicid').annotate( max=Max('date'), freq=Count('postid'), contributors=Count('author', distinct=True)).order_by('-max').get('post')
    # info_model = InfoModel.objects.all().values('topicid').annotate( max=Max('date'), freq=Count('postid'), contributors=Count('author', distinct=True)).order_by('-max').filter('date'__date='max')
    # info_model = InfoModel.objects.all().values('topicid').annotate( max=Max('date'), freq=Count('postid'), contributors=Count('author', distinct=True)).order_by('-max')
    # info_model = InfoModel.objects.all().extra(select={"post": 'post'}).values('topicid').annotate( max=Max('date'), freq=Count('postid'), contributors=Count('author', distinct=True)).order_by('-max')
    # info_model = InfoModel.objects.all().values('topicid').annotate( max=Max('date'), freq=Count('postid'), contributors=Count('author', distinct=True)).order_by('-max').extra(select={"post": 'post'})
    # info_model = InfoModel.objects.all().extra(select={"post": 'post'}).values('topicid').annotate( max=Max('date'), freq=Count('postid'), contributors=Count('author', distinct=True)).order_by('-max')
    # info_model = InfoModel.objects.all().extra(select={"post": 'post'}).values('topicid').annotate( max=Max('date'), freq=Count('postid'), contributors=Count('author', distinct=True)).order_by('-max')
    # info_model = InfoModel.objects.extra(select={"post": 'post'}).values('topicid').annotate( max=Max('date'), freq=Count('postid'), contributors=Count('author', distinct=True)).order_by('-max')
    # info_model = InfoModel.objects.extra(select={'post': 'post'}).values('topicid').annotate( max=Max('date'), freq=Count('postid'), contributors=Count('author', distinct=True)).order_by('-max')
    info_model = InfoModel.objects.values('topicid').annotate( max=Max('date'), freq=Count('postid'), contributors=Count('author', distinct=True)).order_by('-max')

    info2 = InfoModel.objects.all()
    # info = TempModel.objects.values('topicid').annotate( max=Max('date')).order_by('-max')

    columnlist = []
    for item in info2:
         columnlist.append([item])

    for item in info_model:
        for i in range(len(columnlist)):
            if item['max'] == columnlist[i][0].date:
                item['author'] = columnlist[i][0].author
                item['post'] = columnlist[i][0].post
                print item['max']

    # info_model = InfoModel.objects.values('topicid').annotate( max=Max('date'), freq=Count('postid'), contributors=Count('author', distinct=True))
    # info_model = list(InfoModel.objects.raw('SELECT *, max(date), count(postid) AS freq, count(DISTINCT author) AS contributors FROM crudapp_infomodel GROUP BY topicid ORDER BY date DESC'))

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

# blog means articles
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
            print '\n' + 'subject: ' + subject + '\n' + 'to_email: ' + to_email + '\n' + 'from_email: ' + from_email + '\n' + message
            send_mail(subject, message, from_email, [to_email])
            return redirect('init')
    else:
        blogform = BlogForm()
    return render(request, 'blog_form.html', {'blogform': blogform})

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


def blog(request, categ):
    if categ == 'all':
        blogModel = BlogModel.objects.all().filter(approved=True).order_by('pub_date').reverse()
    else:
        blogModel = BlogModel.objects.filter(categories=categ).filter(approved=True).order_by('pub_date').reverse()

    paginator = Paginator(blogModel, 6)
    page = request.GET.get('blog')
    try:
        blog_model = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blog_model = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blog_model = paginator.page(paginator.num_pages)

    context = {'blog_model': blog_model }
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

    return render(request, 'site_users.html', {'users_model': users_model, 'current_time': timezone.now()})

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
