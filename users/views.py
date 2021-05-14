from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, TemplateView
from django.urls import reverse

from .models import User
from .forms import RegistrationForm, LoginForm
from posts.models import Post


class RegistrationView(CreateView):
    template_name = 'users/register.html'
    form_class = RegistrationForm

    def get_context_data(self, *args, **kwargs):
        context = super(RegistrationView, self).get_context_data(*args, **kwargs)
        context['next'] = self.request.GET.get('next')
        return context

    def get_success_url(self):
        next_url = self.request.POST.get('next')
        success_url = reverse('login')
        if next_url:
            success_url += '?next={}'.format(next_url)

        return success_url


class UpdateProfile(UpdateView):
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


class ProfileView(TemplateView):
    template_name = "users/profile-page.html"
