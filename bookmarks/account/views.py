from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm



def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], # it authenticates the user with what we have in a database - it returns a User object or None
                                password=cd['password'])
            if user is not None:
                if user.is_active: # the attribute of a User object
                    login(request, user) # it creates a session for a user.
                    return HttpResponse('Success')
                else:
                    return HttpResponse('The account is blocked')
            else:
                return HttpResponse('Invalid credentials')
    else:
        form = LoginForm()
    
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    """checking if a user is authorized. If so, the view from dashboard.html is displayed. If the 
    user is not logged in, he will be directed to the log-in site and then to the url he wanted access
    - a hidden type next is responsible for that"""
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})