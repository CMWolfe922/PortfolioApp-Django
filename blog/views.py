from django.shortcuts import render
from blog.models import Post, Comment
# I have to import the form I created.
from .forms import CommentForm

# Create your views here.
# create the index view for blog


def blog_index(request):
    posts = Post.objects.all().order_by('-created_on')
    context = {
        "posts": posts,
    }
    return render(request, "blog_index.html", context)


def blog_category(request, category):
    posts = Post.objects.filter(
        categories_name_contains=category).order_by('-created_on')
    context = {
        "category": category,
        "posts": posts
    }
    return render(request, "blog_category.html", context)

# now create the blog detail view


def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)

    # Updated area to accomodate my Django form I created to post comments
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post
            )
            comment.save()

    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        # add the form to context
        "form": form,
    }

    return render(request, "blog_detail.html", context)
