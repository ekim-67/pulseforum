from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from blog.models import Comment, Club
from django.http import Http404, HttpResponseForbidden

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio', 'favorite_book']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name', 'current_book', 'description']

class ClubUpdateForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name', 'description', 'banner']
