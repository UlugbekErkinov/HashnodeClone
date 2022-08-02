from django.shortcuts import render

# Create your views here.from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator
from itertools import chain
from django.db.models import Count
import re
from rest_framework import generics

from feed.serializers import AuthorSerializer, TagSerializer, PostSerializer, CommentSerializer, BookmarkSerializer

from .forms import (AuthorForm, AuthorProfileForm, PostForm,
                    AuthorEditForm, CommentForm)
from .models import Post, Comment, Bookmark, Tag
from author.models import Author

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta

# Create your views here.


class IndexView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_class = [IsAuthenticated, ]

    def get_queryset(self, request):
        tags = request.query_params.get('tags', None)
        return Post.objects.filter(personalize = 'personalized', recent=timezone.now(), is_featured='is_featured', ).order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            posts = self.request.user.profile.followed_posts()
            if posts:
                context['personalized_posts'] = posts[:10]
        return context


class TagsListView(generics.RetrieveAPIView):
   
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_class = [IsAuthenticated, ]

    tags = Tag.objects.annotate(
        total_tags=Count('tags')
    ).order_by('-total_tags')

    # def get_queryset(self):
    #     return Post.objects.filter(tags__name__in=[self.kwargs['posts']])


class DraftsListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_class = [IsAuthenticated, ]

    def get_queryset(self):
        return Post.objects.filter(published_date=None, author=self.request.user).prefetch_related('draft')


class SearchListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_class = [IsAuthenticated, ]
    

    def get_queryset(self):
        search = self.request.GET.get('search')
        return Post.objects.filter(Q(published_date__lte=timezone.now()),
                                   Q(title__contains=search) | Q(content__contains=search)).order_by('-published_date')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet
        context['search'] = self.request.GET.get('search')
        return context





class TagsTrendingListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_class = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = Tag.objects.prefetch_related('tags').annotate(
            total_created=Count('tags')).filter(created_at__gte=7)
        return queryset

class TrendingPostView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_class = [IsAuthenticated, ]

    def get_queryset(self):
        one_week = datetime.today() - timedelta(days=7)
        queryset = Post.objects.annotate(
            total_views=Count('viewers')
        ).filter(report_by_date__gte=one_week).order_by('-total_views')
        return queryset

class NewPostView(LoginRequiredMixin, generics.ListCreateAPIView):
    form_class = PostForm
    model = Post
    queryset = Post.objects.order_by('-published_date')
    serializer_class = PostSerializer
    permission_class = [IsAuthenticated, ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, generics.DestroyAPIView):
    serializer_class = PostSerializer
    permission_class = [IsAuthenticated, ]


class PostDetailView(generics.RetrieveAPIView):
    model = Post
    queryset = Post.objects.all()
  
    serializer_class = PostSerializer
    permission_class = [IsAuthenticated, ]


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


class ProfileDetailView(generics.RetrieveAPIView):
    
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_class = [IsAuthenticated, ]


class PostEditView(LoginRequiredMixin, generics.UpdateAPIView):
    form_class = PostForm
    model = Post
    queryset = Post.objects.all()[:1]
    serializer_class = PostSerializer


class BookMarkListView(LoginRequiredMixin, generics.ListAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

   


def add_comment(request, pk):
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = Post.objects.get(pk=pk)
            comment.author = request.user
            comment.save()
    return HttpResponseRedirect(reverse('hashnode:post', kwargs={'pk': pk}))


def my_profile(request):
    return render(request, 'hashnode/me.html', {'hashnode_user': request.user})


def register_user(request):
    registered = False

    if request.method == 'POST':
        user_form = AuthorForm(data=request.POST)
        user_profile_form = AuthorProfileForm(data=request.POST)

        if user_form.is_valid() and user_profile_form.is_valid():
            new_user = user_form.save()
            new_user.set_password(new_user.password)
            new_user.save()

            new_user_profile = user_profile_form.save(commit=False)
            new_user_profile.user = new_user

            if 'avatar' in request.FILES:
                new_user_profile.avatar = request.FILES['avatar']

            new_user_profile.save()
            registered = True
        else:
            print(user_form.errors, user_profile_form.errors)
    else:
        user_form = AuthorForm()
        user_profile_form = AuthorProfileForm()
    return render(request, 'hashnode/registration.html', {
        'user_form': user_form,
        'user_profile_form': user_profile_form,
        'registered': registered
    })


def new_post(request):

    if request.method == 'POST':
        post_form = PostForm(data=request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()

            if 'image' in request.FILES:

                post.avatar = request.FILES['image']
                post.save()

    else:
        post_form = PostForm()

    return render(request, 'hashnode/new_post.html', {'form': post_form, })


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('hashnode:index'))
        else:
            return HttpResponse('invalid login details')
    else:
        return render(request, 'hashnode/login.html')


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return HttpResponseRedirect(reverse('hashnode:post', kwargs={'pk': pk}))


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('hashnode:index'))


@login_required
def profile_edit(request):

    if request.method == 'POST':
        user_form = AuthorEditForm(data=request.POST, instance=request.user)
        user_profile_form = AuthorProfileForm(
            data=request.POST, instance=request.user.profile)
        user_form.save()
        user_profile = user_profile_form.save()

        if 'avatar' in request.FILES:
            user_profile.avatar = request.FILES['avatar']
        user_profile.save()

        return HttpResponseRedirect(reverse('hashnode:me_edit'))
    else:
        user_form = AuthorEditForm(instance=request.user)
        user_profile_form = AuthorProfileForm(instance=request.user.profile)
        return render(request, 'hashnode/profile_edit.html', {
            'user_profile_form': user_profile_form,
            'user_form': user_form,
        })


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('hashnode:post', pk=post_pk)


@login_required
def follow_user(request, author_pk, post_pk):
    user = Author.objects.get(user=request.user)
    print(user)
    # user.followed_users += str(author) + ','
    follow = Author.objects.get(user=author_pk)
    print(follow)
    user.following.add(follow)
    user.save()
    return redirect('hashnode:post', pk=post_pk)
    # followed_users += user + ', '


@login_required
def unfollow_user(request, author_pk, post_pk):
    user = Author.objects.get(user=request.user)
    print(user)
    # user.followed_users += str(author) + ','
    follow = Author.objects.get(user=author_pk)
    print(follow)
    user.following.remove(follow)
    user.save()
    return redirect('hashnode:post', pk=post_pk)
    # followed_users += user + ', '


@login_required
def follow_tag(request, tag):
    user = Author.objects.get(user=request.user)
    user.followed_tags.add(tag)
    user.save()
    return redirect('hashnode:tags', tag=tag)


@login_required
def unfollow_tag(request, tag):
    user = Author.objects.get(user=request.user)
    user.followed_tags.remove(tag)
    user.save()
    return redirect('hashnode:tags', tag=tag)


@login_required
def unfollow_author(request, tag):
    user = Author.objects.get(user=request.user)
    user.followed_author.remove(tag)
    user.save()
    return redirect('hashnode:tags', tag=tag)


@login_required
def add_emoji(request, pk):
    post = Post.objects.get(pk=pk)
    post.emoji.add(request.user)
    post.save()
    return redirect('hashnode:post', pk=pk)


@login_required
def remove_emoji(request, pk):
    post = Post.objects.get(pk=pk)
    post.emoji.remove(request.user)
    post.save()
    return redirect('hashnode:post', pk=pk)
