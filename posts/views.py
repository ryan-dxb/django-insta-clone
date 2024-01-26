import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from posts.forms import PostCreateForm, PostEditForm, CommentCreateForm, ReplyCreateForm
from posts.models import Post, Tag, Comments, Reply


# Create your views here.


def home_view(request, category_slug=None):
    tag = None

    if category_slug is None:
        posts = Post.objects.all()
    else:
        posts = Post.objects.filter(tags__slug=category_slug)
        tag = get_object_or_404(Tag, slug=category_slug)

    categories = Tag.objects.all()

    context = {"posts": posts, "categories": categories, "tag": tag}

    return render(request, "posts/home.html", context)


@login_required
def post_create_view(request):
    form = PostCreateForm()
    context = {"form": form}

    if request.method == "POST":
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)

            website = requests.get(form.data["url"])
            sourcecode = BeautifulSoup(website.text, "html.parser")
            find_image = sourcecode.select(
                'meta[content^="https://live.staticflickr.com/"]'
            )
            find_title = sourcecode.select("h1.photo-title")
            find_artist = sourcecode.select("a.owner-name")

            try:
                image = find_image[0]["content"]
            except:
                return redirect("post_create_view")

            try:
                title = find_title[0].text.strip()
            except:
                return redirect("post_create_view")

            try:
                artist = find_artist[0].text.strip()
            except:
                return redirect("post_create_view")

            post.image = image
            post.title = title
            post.artist = artist
            post.author = request.user
            post.save()
            form.save_m2m()  # Required when commit=False

            return redirect("home_view")

    return render(request, "posts/post_create.html", context)


@login_required
def post_delete_view(request, pk):
    post = Post.objects.get(id=pk, author=request.user)

    context = {"post": post}

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully")
        return redirect("home_view")

    return render(request, "posts/post_delete.html", context)


@login_required
def post_edit_view(request, pk):
    post = Post.objects.get(id=pk, author=request.user)
    form = PostEditForm(instance=post)

    context = {"post": post, "form": form}

    if request.method == "POST":
        form = PostEditForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully!")
            return redirect("home_view")

    return render(request, "posts/post_edit.html", context)


def post_detail_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    commentform = CommentCreateForm()
    replyform = ReplyCreateForm()

    context = {"post": post, "commentform": commentform, "replyform": replyform}

    return render(request, "posts/post_page.html", context)


@login_required
def comment_sent(request, pk):
    post = get_object_or_404(Post, id=pk)
    # replyform = ReplyCreateForm()

    if request.method == "POST":
        form = CommentCreateForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()

    context = {
        "post": post,
        "comment": comment,
        # 'replyform': replyform
    }

    return redirect("post-detail", post.id)
    # return render(request, "snippets/add_comment.html", context)


@login_required
def comment_delete_view(request, pk):
    post = get_object_or_404(Comments, id=pk, author=request.user)

    if request.method == "POST":
        post.delete()
        messages.success(request, "Comment deleted")
        return redirect("post-detail", post.parent_post.id)

    return render(request, "posts/comment_delete.html", {"comment": post})


@login_required
def reply_sent(request, pk):
    comment = get_object_or_404(Comments, id=pk)
    replyform = ReplyCreateForm()

    if request.method == "POST":
        form = ReplyCreateForm(request.POST)
        if form.is_valid:
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_comment = comment
            reply.save()

    return redirect("post-detail", comment.parent_post.id)


@login_required
def reply_delete_view(request, pk):
    reply = get_object_or_404(Reply, id=pk, author=request.user)

    if request.method == "POST":
        reply.delete()
        messages.success(request, "Comment deleted")
        return redirect("post-detail", reply.parent_comment.parent_post.id)

    return render(request, "posts/reply_delete.html", {"reply": reply})


def like_toggle(model):
    def inner_func(func):
        def wrapper(request, *args, **kwargs):
            post = get_object_or_404(model, id=kwargs.get("pk"))
            user_exist = post.likes.filter(username=request.user.username).exists()

            if post.author != request.user:
                if user_exist:
                    post.likes.remove(request.user)
                else:
                    post.likes.add(request.user)

            return func(request, post)

        return wrapper

    return inner_func


@login_required
@like_toggle(Post)
def like_post(request, post):
    return render(request, "snippets/likes.html", {"post": post})


@login_required
@like_toggle(Comments)
def like_comment(request, post):
    return render(request, "snippets/likes_comment.html", {"comment": post})


@login_required
@like_toggle(Reply)
def like_reply(request, post):
    return render(request, "snippets/likes_reply.html", {"reply": post})
