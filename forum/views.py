from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Post
from .forms import PostForm, CommentForm

def forum_home(request):
    posts_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts_list, 10)  # 10 posts par page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, 'forum/forum_home.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('-created_at')
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Vous devez être connecté pour commenter.')
            return redirect('login')
        
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Commentaire ajouté avec succès!')
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()
    
    return render(request, 'forum/post_detail.html', {
        'post': post, 
        'comments': comments, 
        'comment_form': comment_form
    })

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Sujet créé avec succès!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    
    return render(request, 'forum/post_form.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        messages.error(request, 'Vous ne pouvez pas modifier ce sujet.')
        return redirect('forum_home')
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sujet modifié avec succès!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'forum/post_form.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        post.delete()
        messages.success(request, 'Sujet supprimé avec succès!')
    else:
        messages.error(request, 'Vous ne pouvez pas supprimer ce sujet.')
    
    return redirect('forum_home')
