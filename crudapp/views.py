from django.shortcuts import render, get_object_or_404
from .models import Members
from django import forms
from .forms import MemberForm
from django.shortcuts import redirect

# Create your views here.
def init(request):
    print 'this is the init view'
    details = reversed(Members.objects.all())
    context = {'details': details}
    return render(request, 'index.html', context)

def member_new(request):
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # post.author = request.user
            # post.published_date = timezone.now()
            print 'this is just BEFORE save'
            post.save()
            print 'this is just after save'
            # return redirect('post_detail', pk=post.pk)
            return redirect('init')
    else:
        form = MemberForm()
    return render(request, 'member_edit.html', {'form': form})

def edit_new(request, id):
    post = get_object_or_404(Members, pk=id)
    if request.method == "POST":
        form = MemberForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False) #don't save model just yet
            print request.user
            # post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('init')
    else:
        form = MemberForm(instance=post)
    return render(request, 'member_edit.html', {'form': form})

def delete_new(request, id):
    post = get_object_or_404(Members, pk=id)
    post.delete()
    return redirect(init)

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
