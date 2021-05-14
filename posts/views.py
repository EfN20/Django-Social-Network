from django.shortcuts import render, redirect, get_object_or_404

from .forms import PostForm
from .models import Post


def post_add(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("/")


def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        action = request.POST['action']
        if action == 'edit':
            new_description = request.POST['description']
            new_img = request.FILES.get('img')
            post.description = new_description
            post.img = new_img
            post.save()
            return redirect('post-edit', post_id)
        if action == 'delete':
            post.delete()
            return redirect('/')
    context = {
        'post': post,
    }
    return render(request, 'posts/post-edit.html', context=context)
