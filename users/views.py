from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CommentForm
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from blog.models import Post, Club
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save() #creates the actual user in the database
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username} !')
            return redirect('login')
    else:   
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form, 'active_page': 'join'})


@login_required
def update_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Profile updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'active_page': 'profile',
    }

    return render(request, 'users/update_profile.html', context)

@login_required
def profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
        author = user.id
    
    else:
        user = request.user
        author = request.user.id

    context = {
        'profile_user': user,
        'posts': Post.objects.filter(author=author),
        'active_page': 'profile',
    }

    return render(request, 'users/profile.html', context)

@login_required
def my_clubs(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user

    if request.method == 'POST':
        clubname = request.POST.get('btn')
        #get the name chosen by the user^
        chosen_club = Club.objects.filter(name=clubname).first()
        user.profile.club.remove(chosen_club)
        return redirect('blog-home')

    context = {
        'profile_user': user,
        'active_page':'groups',
    }

    return render(request, 'users/my_clubs.html', context)