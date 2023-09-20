from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView,DetailView
from . models import BlogPost,Comment
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BlogPost
from . form import BlogForm,CommentForm



def log_in(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        password_r = request.POST.get('password')
        user = authenticate(request, username=name_r, password=password_r)
        if user:
            login(request, user)
            return redirect('home')

        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'login.html', context)
    else:
        context["error"] = "You are not logged in"
        return render(request, 'login.html', context)


def register(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        email_r = request.POST.get('email')
        password_r = request.POST.get('password')
        user = User.objects.create_user(name_r, email_r, password_r, )
        if user:
            messages.info(request, "You have successfully register.")
            return render(request, 'login.html')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'register.html', context)
    else:
        return render(request, 'register.html', context)
    


def home(request):
    blog=BlogPost.objects.all()
    return render(request,'home.html',{'blog':blog})


class BlogCreateView(CreateView):
    model=BlogPost
    template_name='create.html'
    fields=['image','title','content','author']
    
    def get_success_url(self):
        return reverse_lazy('home')
    
def add_comment(request, post_id):
    if request.method == 'POST':
        text = request.POST['comment']
        post = BlogPost.objects.get(id=post_id)
        author = request.user

        # Create a new comment
        comment = Comment(post=post, author=author, text=text)
        comment.save()
        messages.success(request, 'Comment added successfully.')

    return redirect('home')


class BlogDetailView(DetailView):
    model=BlogPost
    template_name='detail.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'blog' 

    def get_success_url(self):
        return reverse_lazy('detail')


@login_required
def edit_blog_post(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)

    
    if request.user == blog_post.author:
        if request.method == "POST":
            form = BlogForm(request.POST, instance=blog_post)
            if form.is_valid():
                form.save()
                return redirect('home')  
        else:
            form = BlogForm(instance=blog_post)

        return render(request, 'update.html', {'form': form, 'blog_post': blog_post})
    else:
        return render(request, 'error.html')

@login_required
def delete_blog_post(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)

    # Check if the current user is the author of the blog post
    if request.user == blog_post.author:
        if request.method == "POST":
            blog_post.delete()
            return redirect('home')  # Redirect to the home page after successful delete

        return render(request, 'delete.html', {'blog_post': blog_post})
    else:
        return render(request, 'error.html')

def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("login")


def comment_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # Create a new comment linked to the post and the current user
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user  # Assuming you have authentication enabled
            new_comment.save()
            # Redirect to the same post page after commenting
            return redirect('detail', pk=pk)
    else:
        form = CommentForm()  # Create a blank form for comment submission

    # Retrieve existing comments for the post
    comments = Comment.objects.filter(post=post)

    return render(request, 'comment.html', {'post': post, 'comments': comments, 'form': form})



