from django.shortcuts import render_to_response


def loggedin(request):
    return render_to_response('registration/loggedin.html')
