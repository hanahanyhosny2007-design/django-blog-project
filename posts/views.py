from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Author, Post, Comment
from .forms import RegisterForm, PostForm, CommentForm
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {
        'posts': posts
    })

def posts(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts.html', {
        'posts': posts
    })

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.all().order_by('-created_at')
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.name = request.user.username
            comment.save()
            return redirect('post_detail', id=post.id)
    else:
        form = CommentForm()
    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Author.objects.create(
                name=user.username,
                email=user.email
            )
            login(request, user)

            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {
        'form': form
    })

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        from django.contrib.auth import authenticate
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            return redirect('home')
        return render(request, 'login.html', {
            'error': 'Invalid username or password.'
        })
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            author, created = Author.objects.get_or_create(
                email=request.user.email,
                defaults={
                    'name': request.user.username
                }
            )
            post.author = author
            post.save()
            return redirect('posts')
    else:
        form = PostForm()

    return render(request, 'create_post.html', {
        'form': form
    })

@login_required
def update_post(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return redirect('post_detail', id=post.id)

    else:
        form = PostForm(instance=post)

    return render(request, 'update_post.html', {
        'form': form,
        'post': post
    })

@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        post.delete()
        return redirect('posts')
    return render(request, 'delete_post.html', {
        'post': post
    })