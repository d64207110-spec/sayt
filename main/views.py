from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from .models import Topic, Post, Profile
from .forms import TopicForm, PostForm, ProfileForm


def is_banned(user):
    if not user.is_authenticated:
        return False
    profile, _ = Profile.objects.get_or_create(user=user)
    return profile.is_banned


def topic_list(request):
    topics = Topic.objects.all().order_by('-created')
    return render(request, 'topic_list.html', {'topics': topics})


def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    banned = is_banned(request.user)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        if banned:
            return HttpResponseForbidden('Вы забанены и не можете писать сообщения.')
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.author = request.user
            post.save()
            return redirect('topic_detail', pk=pk)
    else:
        form = PostForm()
    return render(request, 'topic_detail.html',
                  {'topic': topic, 'form': form, 'banned': banned})


@login_required
def topic_new(request):
    if is_banned(request.user):
        return HttpResponseForbidden('Вы забанены и не можете создавать темы.')
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = Topic.objects.create(title=form.cleaned_data['title'], author=request.user)
            Post.objects.create(topic=topic, author=request.user, text=form.cleaned_data['text'])
            return redirect('topic_detail', pk=topic.pk)
    else:
        form = TopicForm()
    return render(request, 'topic_new.html', {'form': form})


@login_required
@require_POST
def topic_delete(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    # удалять может только админ или создатель темы
    if not (request.user.is_staff or request.user == topic.author):
        return HttpResponseForbidden('Нет прав на удаление этой темы.')
    topic.delete()
    return redirect('topic_list')


@login_required
@require_POST
def user_ban(request, username):
    if not request.user.is_staff:
        return HttpResponseForbidden('Только админ может банить.')
    target = get_object_or_404(User, username=username)
    if target.is_staff or target == request.user:
        messages.error(request, 'Нельзя забанить администратора или себя.')
        return redirect('profile', username=username)
    profile, _ = Profile.objects.get_or_create(user=target)
    profile.is_banned = True
    profile.save()
    return redirect('profile', username=username)


@login_required
@require_POST
def user_unban(request, username):
    if not request.user.is_staff:
        return HttpResponseForbidden('Только админ может разбанивать.')
    target = get_object_or_404(User, username=username)
    profile, _ = Profile.objects.get_or_create(user=target)
    profile.is_banned = False
    profile.save()
    return redirect('profile', username=username)


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