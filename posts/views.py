from django.forms import ModelForm, Textarea
from django.shortcuts import render, redirect

from posts.models import Post


# Create your views here.


def home_view(request):
    posts = Post.objects.all()

    context = {"posts": posts}
    return render(request, "posts/home.html", context)


class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        labels = {"body": "Caption"}
        widgets = {
            "body": Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Add a caption...",
                    "class": "font1 text-4xl",
                }
            )
        }


def post_create_view(request):
    form = PostCreateForm()
    context = {"form": form}

    if request.method == "POST":
        form = PostCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home_view")

    return render(request, "posts/post_create.html", context)
