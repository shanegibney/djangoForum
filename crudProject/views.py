from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf

def loggedin(request):
    # return render_to_response('registration/loggedin.html')
    return redirect('init')

# def loggedin(request):
#     return render_to_response('registration/loggedin.html',
#                               {'username': request.user.username})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # return HttpResponseRedirect('/accounts/register/complete')
            return redirect('init')

    else:
        form = UserCreationForm()
    token = {}
    token.update(csrf(request))
    token['form'] = form

    return render_to_response('registration/registration_form.html', token)

def registration_complete(request):
    # return render_to_response('registration/registration_complete.html')
    return redirect('init')
