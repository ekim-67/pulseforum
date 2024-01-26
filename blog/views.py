from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Post, Comment, Club
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.views import View
from users.forms import CommentForm, ClubForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.shortcuts import get_object_or_404


def home(request):
    club = get_object_or_404(Club, pk=1)

    context = {
        'posts': club.post_set.all(),
        'members': User.objects.all(),
        'club':club,
        'is_member':True,
    }
    #for the third argument, passing in a dictionary with a single entry -- pointing to a list of dictionaries inside it. 

    return render(request, 'blog/home.html', context)

def clubHome(request, pk):
    club = get_object_or_404(Club, pk=pk)

    is_member = False

    if request.user.profile in club.profile_set.all():
        is_member = True

    context = {
        'posts': Post.objects.filter(club=club),
        'members': User.objects.all(),
        'club': club,
        'is_member': is_member,
    }
    #for the third argument, passing in a dictionary with a single entry -- pointing to a list of dictionaries inside it. 

    return render(request, 'blog/club_home.html', context)

def create_club(request):
    if request.method == 'POST':
        form = ClubForm(request.POST)
        if form.is_valid():
            new_club = form.save(commit=False)
            user = request.user
            new_club.owner = user
            form.save()
            user.profile.club.add(new_club)
            return redirect('blog-home')
    else:
        form = ClubForm()
    return render(request, 'blog/create_club.html', {'form':form})

def club_list(request): #includes means of joining club
    clubs = Club.objects.all()
    user = request.user
    if request.method == 'POST':
        clubname = request.POST.get('btn')
        #get the name chosen by the user^
        chosen_club = Club.objects.filter(name=clubname).first()
        user.profile.club.add(chosen_club)

        context = {
            'posts': Post.objects.filter(club=chosen_club),
            'members': User.objects.all(),
            'club': chosen_club,
            'is_member': True,
        }
        return render(request, 'blog/club_home.html', context)
    
    return render(request, 'blog/club_list.html', {'clubs': clubs})

class PostListView(ListView):
    model = Post #tells the ListView what model to query to create the list
    template_name = 'blog/home.html' #overriding template_name variable
    context_object_name = 'posts' #sets it so that you loop over 'posts' instead
    ordering = ['-date_posted'] #sets the posts from newest to oldest

    def get_context_data(self,**kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['members'] = User.objects.all()
        return context

#<app>/<model>_<viewtype>.html
#blog/post_list.html
#by default, it loops over "object_list"

class MemberListView(ListView):
    model = User
    template_name = 'blog/member_list.html'
    context_object_name = 'members'

def comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog-home')
    
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post 
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['author'] = self.get_object().author
        return context
    
    def post(self, request, *args, **kwargs):
        if 'post-comment' in request.POST:
            form = CommentForm(request.POST)
            #author = self.get_object().author
            #post = self.get_object()

            if form.is_valid():
                #import pdb; pdb.set_trace()
                #form.author = author
                #form.post = post
                new_comment = form.save(commit=False)
                new_comment.author = request.user
                new_comment.post = self.get_object()
                new_comment.save()

                return HttpResponseRedirect(self.request.path_info)

#    def get_success_url(self):
#        return reverse('author-detail', kwargs={'pk': self.object.pk})

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.club = Club.objects.get(pk=self.kwargs.get('club_id'))
        return super().form_valid(form) 
        #sets the author variable before the parent class runs the function
    
    #def save(self, *args, **kwargs):
    #    super(Post, self).save(*args, **kwargs)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form) 
        #sets the author variable before the parent class runs the function
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False
        
@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    if request.user.id == comment.author.id:
        Comment.objects.get(pk=pk).delete()
    return redirect('post-detail', pk=post_pk)
    
def about(request):

    #for the third argument, passing in a single dictionary entry

    return render(request, 'blog/about.html', {'title': 'About'})

