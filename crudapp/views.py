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
# from models import EmailForm


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
    blogModel = reversed(BlogModel.objects.all())
    context = {'blogModel': blogModel}
    return render(request, 'blog.html', context)

# Create your views here.
def init(request):
    pModel = PostModel.objects.raw('SELECT *, max(pub_date), count(topic_id) AS freq FROM crudapp_postmodel GROUP BY topic_id ORDER BY pub_date DESC LIMIT 0,20')
    totalposts = PostModel.objects.annotate(Count('post'))
    totaltopics = TopicModel.objects.annotate(postfreq = Count('topic'))
    totalusers = User.objects.annotate(postfreq = Count('id'))
    totalviews = TopicModel.objects.aggregate(numviews = Sum('views'))
    # pModel = PostModel.objects.raw('select *, max(pub_date) from crudapp_postmodel WHERE topic_id = )
    # num = PostModel.objects.raw('select count(id) from crudapp_postmodel group by topicid_id')
    context = {'pModel': pModel, 'current_time':   timezone.now(), 'totalposts': totalposts, 'totaltopics': totaltopics, 'totalusers': totalusers, 'totalviews': totalviews}
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
    pModel = reversed(PostModel.objects.all().filter(author = profileof))
    pnumber = PostModel.objects.filter(author = profileof).annotate(postfreq = Count('post'))
    # this line below is not correct, it is counting the number of topics started by the author
    tnumber = PostModel.objects.filter(author = profileof).values('topic_id').distinct().annotate(topicfreq = Count('topic_id'))
    # count = Project.objects.values('informationunit__username').distinct().count()
    return render(request, 'profile.html', {'pModel': pModel, 'current_time': timezone.now(), 'name': profileof, 'pnumber': pnumber, 'tnumber': tnumber})


def site_users(request):
    site_users = User.objects.all()
    return render(request, 'site_users.html', {'site_users': site_users})

#display thread of posts and form for next post
def thread(request, id):
    if request.method == "POST":
        pk = id
        userInstance = User.objects.get(username = request.user)
        tform = get_object_or_404(TopicModel, pk = id)
        # Pform = PostForm(request.POST, instance=tform)
        Pform = PostForm(request.POST)
        # tform = TopicModel.objects.get(pk=id)
        if Pform.is_valid():
            tform.author = userInstance
            # tform.save()
            pform = Pform.save(commit=False)
            pform.topic = tform
            pform.author = request.user
            pform.user = userInstance
            pform.pub_date = timezone.now()
            pform.save()
            # return redirect('post_detail', pk=post.pk)
            return redirect('thread', id)
    else:
        pk=id
        pModel = reversed(PostModel.objects.all().filter(topic_id = pk))
        postform = PostForm()
        post = get_object_or_404(TopicModel, pk = id)
        post.views += 1
        post.save()
        # name = str(post.author)
        threadTopic = reversed(TopicModel.objects.all().filter(id = pk))
        num = id
        # How many posts are there for this topic_id
        numtopicposts = PostModel.objects.all().filter(topic_id = pk).annotate(postfreq = Count('post'))
        numtopicusers = PostModel.objects.all().filter(topic_id = pk).values('author').distinct().annotate(authorfreq = Count('author'))
        context = {'pModel': pModel, 'postform' : postform, 'current_time': timezone.now(), 'threadTopic': threadTopic, 'numtopicposts': numtopicposts, 'numtopicusers': numtopicusers}
    return render(request, 'thread.html', context)

#create new post
# def topic_new(request):
#     if request.method == "POST":
#         form = MemberForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.pub_date = timezone.now()
#             post.save()
#             # return redirect('post_detail', pk=post.pk)
#             return redirect('init')
#     else:
#         form = MemberForm()
#     return render(request, 'member_edit.html', {'form': form})


# def edit_post(request, thread_id, post_id):# example from wearesocial
#form for topic and first post also used to edit posts
def topic_form(request):
    if request.method == "POST":
        # userInstance = get_object_or_404(User, username = request.user)
        # using .get() because there is only one each user has a unique record
        userInstance = User.objects.get(username = request.user)
        Tform = TopicForm(request.POST)
        Pform = PostForm(request.POST)
        # From Django Documentation
        # >>> from blog.models import Entry
        # >>> entry = Entry.objects.get(pk=1)
        # >>> cheese_blog = Blog.objects.get(name="Cheddar Talk")
        # >>> entry.blog = cheese_blog
        # >>> entry.save()
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
    # post.delete()
    form = PostForm(instance=post)
    # post.post = "This post was removed by " + str(request.user)
    post.post = "This post has been removed by the author"
    post.save()
    #id is the post's id and is used to get the id of the topic
    #id to be sent needs to be the topicid_id
    id = post.topic_id#this is the id of the topic
    return redirect('thread', id)

# def post_detail(request, pk):
#     print 'this is the post_detail view'
#     # post = get_object_or_404(Members, pk=pk)
#     # return render(request, 'post_detail.html', {'post': post})
#     return redirect('init')

# def get_name(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = NameForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponseRedirect('index.html')
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = NameForm()
#
#     return render(request, 'index.html', {'form': form})


# def details(request):
#     ip = request.META['REMOTE_ADDR']
#     context = {'ip': ip}
#     return render(request, 'details.html', context)



# def contact(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         # if form.is_valid():
#         #     cd = form.cleaned_data
#         #     send_mail(
#         #         cd['subject'],
#         #         cd['message'],
#         #         cd.get('email', 'noreply@example.com'),
#         #         ['siteowner@example.com'],
#         #     )
#         return HttpResponseRedirect('')
#     # else:
#     #     form = ContactForm()
#     # return render(request, 'contact_form.html', {'form': form})
#
#
# def contact(request):
#     errors = []
#     if request.method == 'POST':
#         if not request.POST.get('firstname', ''):
#             errors.append('Enter a first name.')
#         if not request.POST.get('lastname', ''):
#             errors.append('Enter a message.')
#         # if request.POST.get('email') and '@' not in request.POST['email']:
#         #     errors.append('Enter a valid e-mail address.')
#         if request.POST.get('descript', ''):
#             errors.append('Enter description.')
#         if not errors:
#
#             # send_mail(
#             #     request.POST['subject'],
#             #     request.POST['message'],
#             #     request.POST['descrip'],
#             # )
#             return HttpResponseRedirect('/contact/thanks/')
#     return render(request, 'contact_form.html',
#         {'errors': errors})


# def display_meta(request):
#     values = request.META.items()
#     values.sort()
#     html = []
#     for k, v in values:
#         html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
#     return HttpResponse('<table>%s</table>' % '\n'.join(html))


# EXAMPLE QUERIES
# tModel = reversed(TopicModel.objects.all())
# pModel = reversed(PostModel.objects.all())
# pModel = reversed(PostModel.objects.filter(topicid_id=pk).order_by('-pub_date')[0])
# p1 = PostModel.objects.order_by('topicid_id')
# p2 = p1.order_by('-pub_date')[0]
# pModel = PostModel.objects.order_by('topicid_id').order_by('-pub_date')[0]
# context = {'tModel': tModel, 'pModel': pModel}
# nums = PostModel.objects.values('topicid').annotate(yoke=Count('post'))

# get the topicid of the which has the latest date
# nums = PostModel.objects.values('topicid').latest('pub_date')

# gives value of all topicid's
# nums = PostModel.objects.values('topicid')

# topics of the latest 20 posts
# nums = PostModel.objects.filter(
#     topicid__gt=0
#     ).distinct().annotate(a_count=Count(
#     'post')
#     ).order_by('-pub_date').filter(a_count__gte=1)[:5]
# theSQL = nums.query
# Reservation.objects.filter(
#     restaurant__city_id__gt=0
#     ).distinct().annotate(city_count=Count(
#     'restaurant_id')
#     ).order_by('-reservationdate').filter(city_count__gte=1)[:20]

# num = PostModel.objects.values('author').annotate(total=Count('post'))#groups by author and counts the posts for each author
# num = PostModel.objects.values('topicid').annotate(most_recent=Count('post')).latest('pub_date')
# num = PostModel.objects.values('topicid').annotate(recent=Count('post'))####
# current =  num[0].recent
# num = PostModel.objects.annotate(Count('author'))
# current = PostModel.objects.latest('pub_date')
# detail = PostModel.objects.values('topicid.topic').aggregate(Max('pub_dat'))
# Book.objects.all().aggregate(Max('price'))
# Transaction.objects.values('order_id').annotate(total=Sum('value'))
