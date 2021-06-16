from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView

from chat.models import Room
from medias.models import Media
from medias.forms import MediaForm
from posts.forms import PostForm
from posts.models import Post
from .forms import RegistrationForm, LoginForm, UserChangeForm
from .models import User, FriendRequest


class RegistrationView(CreateView):
    template_name = 'users/register.html'
    form_class = RegistrationForm

    def get_context_data(self, *args, **kwargs):
        context = super(RegistrationView, self).get_context_data(*args, **kwargs)
        context['next'] = self.request.GET.get('next')
        return context

    def get_success_url(self):
        next_url = self.request.POST.get('next')
        success_url = reverse('login/')
        if next_url:
            success_url += '?next={}'.format(next_url)

        return success_url


class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = User
    # fields = ['name', 'tag', 'phone_number', 'date_of_birth', 'avatar']
    form_class = UserChangeForm
    template_name = 'users/edit-profile.html'

    def get_success_url(self):
        return reverse('users:profile')

    def get_object(self):
        return self.request.user


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        posts = Post.objects.filter(user__in=self.request.user.friend_list.all())
        my_posts = Post.objects.filter(user=self.request.user)
        posts |= my_posts
        posts = posts.order_by('-post_date')
        return posts

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        form = PostForm()
        context['post_form'] = form
        media_form = MediaForm()
        context['story_form'] = media_form
        date_from = datetime.now() - timedelta(days=1)
        friends_media = Media.objects.filter(user__in=self.request.user.friend_list.all())
        friends_id_list = Media.objects.filter(user__in=self.request.user.friend_list.all(), posted_date__gte=date_from).values_list('user').distinct()
        print(list(friends_id_list))
        friends_list = User.objects.filter(user_id__in=list(friends_id_list))
        print(friends_list)
        context['friends_stories'] = friends_media
        for media in friends_media:
            print(media.user)
            print(media.extension())
            print(media.file.url)
        context['friends_list'] = friends_list
        return context


def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("/")
    if request.POST:
        form = LoginForm(request.POST)
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        print(phone_number, password)
        user = authenticate(phone_number=phone_number, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged In")
            return redirect("/")
        else:
            messages.error(request, "please Correct Below Errors")
    else:
        form = LoginForm()
    context['login_form'] = form
    return render(request, "users/login.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, "Logged Out")
    return redirect("/login")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile-page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.filter(user=self.request.user)
        posts = posts.order_by('-post_date')
        context['posts'] = posts
        form = PostForm()
        context['post_form'] = form
        return context


@login_required
def send_friend_request(request, user_to):
    user_from = request.user
    user_to = User.objects.get(id=user_to)
    if user_from == user_to:
        return HttpResponse('Cannot send request to yourself :)')
    if user_from in user_to.friend_list.all():
        return HttpResponse('Already in friend list')
    friend_request, created = FriendRequest.objects.get_or_create(user_from=user_from, user_to=user_to)
    if created:
        return HttpResponse('Friend request sent')
    else:
        return HttpResponse('Request was already sent')


@login_required
def accept_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.user_to == request.user:
        friend_request.user_to.friend_list.add(friend_request.user_from)
        friend_request.user_from.friend_list.add(friend_request.user_to)
        friend_request.delete()
        return HttpResponse('Friend request accepted')


class FriendsView(LoginRequiredMixin, ListView):
    template_name = 'users/friend-page.html'
    model = User

    def get_context_data(self, *args, **kwargs):
        context = super(FriendsView, self).get_context_data(*args, **kwargs)
        context['friends'] = self.request.user.friend_list.all()
        context['requests'] = FriendRequest.objects.filter(user_to=self.request.user)
        context['rooms'] = Room.objects.filter(members=self.request.user, type=False)
        return context


@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):
    user.is_online = True
    user.last_login = datetime.now()
    user.save()


@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):
    user.is_online = False
    user.save()
