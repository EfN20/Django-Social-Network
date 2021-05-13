from django.shortcuts import render, redirect, get_object_or_404

from .models import *


def PostAddView(request):
    posts = Post.objects.all()
    if request.method == 'POST':
        title = request.POST['title']
        text = request.POST['text']
        Post.objects.create(user=request.user, title=title, description=text)

    context = {
        'posts': posts,
    }
    return render(request, 'posts/post-add.html', context=context)


def PostEditView(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        type = request.POST['type']
        if type == 'edit':
            new_title = request.POST['title']
            new_text = request.POST['text']
            new_img = request.FILES.get('img')
            post.title = new_title
            post.description = new_text
            post.img = new_img
            post.save()
            return redirect('post-edit', post_id)
        if type == 'delete':
            post.delete()
            return redirect('main-page')
    context={
        'post': post,
    }
    return render(request, 'posts/post-edit.html', context=context)
