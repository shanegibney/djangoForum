from django.shortcuts import render, get_object_or_404, redirect
from .models import Members, TopicModel, PostModel
from django.db.models import Count, Max
from django import forms
from .forms import MemberForm, TopicForm, PostForm
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
    pModel = PostModel.objects.raw('select *, max(pub_date) from crudapp_postmodel group by topicid_id order by pub_date desc LIMIT 0,10')
    print 'pModel: %s' %pModel
    context = {'pModel': pModel, 'current_time': timezone.now()}
    return render(request, 'forum.html', context)


#display thread of posts and form for next post
def thread(request, id):
    if request.method == "POST":
        print 'we are inside POST'
        pk = id
        tform = get_object_or_404(TopicModel, pk=id)
        # Pform = PostForm(request.POST, instance=tform)
        Pform = PostForm(request.POST)
        # tform = TopicModel.objects.get(pk=id)
        if Pform.is_valid():
            pform = Pform.save(commit=False)
            pform.topicid = tform
            pform.author = request.user
            pform.pub_date = timezone.now()
            pform.save()
            # return redirect('post_detail', pk=post.pk)
            return redirect('thread', id)
    else:
        pk=id
        print 'topic pk is : %s' %pk
        pModel = reversed(PostModel.objects.all().filter(topicid_id=pk))
        # threadTopic = reversed(TopicModel.objects.all().filter(id=pk))
        # threadTopic = TopicModel.objects.raw('select topic from crudapp_topicmodel where id = %d', [pk])
        postform = PostForm()
        # print 'threadTopic is %s' %threadTopic
        # for yoke in threadTopic:
        #     print 'oops'
        #     topic = yoke.topicid.topic
        # print 'topic is: %s' %topic
    return render(request, 'thread.html', {'pModel': pModel, 'postform' : postform, 'current_time': timezone.now()})
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
#form for topic and first post
def topic_form(request):
    if request.method == "POST":
        Tform = TopicForm(request.POST)
        Pform = PostForm(request.POST)
        if Tform.is_valid() and Pform.is_valid():
            tform = Tform.save(commit=False)
            # tform.extra = 'blah'
            tform.topicAuthor = request.user
            tform.save() #returns request and id
            pform = Pform.save(commit=False)
            pform.topicid = tform
            print 'pform.topicid: %s' %pform.topicid
            pform.author = request.user
            pform.pub_date = timezone.now()
            pform.save()
            return redirect('init')
    else:
        topicform = TopicForm()
        postform = PostForm()
    return render(request, 'new_topic.html', {'topicform': topicform, 'postform': postform})

#edit a post
def edit_new(request, id):
    post = get_object_or_404(PostModel, pk=id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False) #don't save model just yet
            # post.author = request.user
            post.pub_date = timezone.now()
            post.save()

            post = get_object_or_404(PostModel, pk=id)
            id = post.topicid_id

            return redirect('thread', id)
    else:
        form = MemberForm(instance=post)
    return render(request, 'member_edit.html', {'form': form})

#delete a post, actually replaces post with a message
def delete_new(request, id):
    post = get_object_or_404(PostModel, pk=id)
    # post.delete()
    form = PostForm(instance=post)
    # post.post = "This post was removed by " + str(request.user)
    post.post = "This post has been removed by the author"
    post.save()
    print 'end of delete id is %s' %id
    #id is the post's id and is used to get the id of the topic
    #id to be sent needs to be the topicid_id
    id = post.topicid_id#this is the id of the topic
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
