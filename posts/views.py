import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from posts.forms import PostCreateForm, PostEditForm
from posts.models import Post, Tag


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
            post.save()
            form.save_m2m()  # Required when commit=False

            return redirect("home_view")

    return render(request, "posts/post_create.html", context)


def post_delete_view(request, pk):
    post = Post.objects.get(id=pk)

    context = {"post": post}

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully")
        return redirect("home_view")

    return render(request, "posts/post_delete.html", context)


def post_edit_view(request, pk):
    post = Post.objects.get(id=pk)
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
    context = {"post": post}

    return render(request, "posts/post_page.html", context)
