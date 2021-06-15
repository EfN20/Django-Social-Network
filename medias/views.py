from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Media
from .forms import MediaForm

from datetime import datetime


@login_required
def media_add(request):
    if request.method == "POST":
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            new_media = form.save(commit=False)
            new_media.user = request.user
            new_media.save()
            return redirect("/")
