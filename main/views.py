from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Topic, Post
from .forms import TopicForm, PostForm
from django.contrib.auth.models import User
from .models import Topic, Post, Profile
from .forms import TopicForm, PostForm, ProfileForm


def topic_list(request):
    topics = Topic.objects.all().order_by('-created')
    return render(request, 'topic_list.html', {'topics': topics})


def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.author = request.user
            post.save()
            return redirect('topic_detail', pk=pk)
    else:
        form = PostForm()
    return render(request, 'topic_detail.html', {'topic': topic, 'form': form})


@login_required
def topic_new(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = Topic.objects.create(title=form.cleaned_data['title'], author=request.user)
            Post.objects.create(topic=topic, author=request.user, text=form.cleaned_data['text'])
            return redirect('topic_detail', pk=topic.pk)
    else:
        form = TopicForm()
    return render(request, 'topic_new.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('topic_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile, _ = Profile.objects.get_or_create(user=profile_user)
    return render(request, 'profile.html', {'profile_user': profile_user, 'profile': profile})


@login_required
def profile_edit(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile_edit.html', {'form': form})