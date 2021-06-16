from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .forms import PostForm
from .models import Post
from .serializers import PostSerializer


@login_required
def post_add(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect(request.META['HTTP_REFERER'])


@login_required
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
            return redirect(request.META['HTTP_REFERER'])
    context = {
        'post': post,
    }
    return render(request, 'posts/post-edit.html', context=context)


@api_view(['POST'])
def post_create(request):
    serializer = PostSerializer(data=request.data)
    print(vars(serializer))
    if serializer.is_valid():
        post = serializer.save(user=request.user, img=request.FILES.get('img'))
        print(vars(post))
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['POST'])
@login_required
def post_update(request, post_id):
    post = Post.objects.get(pk=post_id)
    serializer = PostSerializer(instance=post, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
@login_required
def post_delete(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.delete()
    return Response("Post has been deleted successfully!")

