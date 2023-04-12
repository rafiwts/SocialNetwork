from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


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


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)

            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    
    return render(request,
                 'account/register.html',
                 {'user_form': user_form})


@login_required
def edit_profile(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
                                        instance=request.user.profile,
                                        data=request.POST,
                                        files=request.FILES
                                    )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "The profile has been successfully edited.")
        else:
            messages.error(request, "Error occured while editing the profile.")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True) # method for checking if a user is active
    return render(request,
                  'account/user/list.html',
                  {'section': 'people',
                   'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, # an active user with a given name/404 if no such user
                             username=username,
                             is_active=True)
    return render(request,
                  'account/user/detail.html',
                  {'section': 'people',
                   'user': user})
    