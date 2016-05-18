from django.shortcuts import render, get_object_or_404, redirect
from .models import TopicModel, PostModel
from django.contrib.auth.models import User
from django.db.models import Count, Max, Sum
from django import forms
from .forms import TopicForm, PostForm
from django.utils import timezone
from datetime import date, timedelta

# Create your views here.
def init(request):
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
    pModel = PostModel.objects.raw('SELECT *, max(pub_date), count(topic_id) AS freq FROM crudapp_postmodel GROUP BY topic_id ORDER BY pub_date DESC LIMIT 0,20')
    totalposts = PostModel.objects.annotate(Count('post'))
    totaltopics = TopicModel.objects.annotate(postfreq = Count('topic'))
    totalusers = User.objects.annotate(postfreq = Count('id'))
    totalviews = TopicModel.objects.aggregate(numviews = Sum('views'))
    # pModel = PostModel.objects.raw('select *, max(pub_date) from crudapp_postmodel WHERE topic_id = )
    # num = PostModel.objects.raw('select count(id) from crudapp_postmodel group by topicid_id')
    context = {'pModel': pModel, 'current_time': timezone.now(), 'totalposts': totalposts, 'totaltopics': totaltopics, 'totalusers': totalusers, 'totalviews': totalviews}
    return render(request, 'forum.html', context)

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
