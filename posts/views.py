from django.http import request
from django.shortcuts import render, redirect, get_object_or_404 , HttpResponse
from posts.models import *


def PostAddView():
    posts = Post.objects.all()
    if request.method == 'POST':
        title = request.POST['title']
        text = request.POST['text']
        Post.objects.create(title=title, text=text)

    context = {
        'posts': posts,
    }
    return render(request, '', context=context)

def PostEditView(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        type = request.POST['type']
        if type == 'edit':
            new_title = request.POST['title']
            new_text = request.POST['text']
            new_img = request.FILES.get('img')
            post.title = new_title
            post.text = new_text
            post.img = new_img
            post.save()
            return redirect('', post_id)
        if type == 'delete':
            post.delete()
            return redirect()
    context={
        'post': post,
    }
    return render(request,'', context=context)