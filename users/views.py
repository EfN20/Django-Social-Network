from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, TemplateView
from django.urls import reverse

from .models import User, FriendRequest
from .forms import RegistrationForm, LoginForm
from posts.models import Post
from posts.forms import PostForm
from chat.models import Room


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
    fields = ['name', 'tag', 'phone_number', 'date_of_birth', 'avatar']
    template_name = 'users/edit-profile.html'

    def get_success_url(self):
        return reverse('index')

    def get_object(self):
        return self.request.user


class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-post_date')

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        form = PostForm()
        context['post_form'] = form
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
