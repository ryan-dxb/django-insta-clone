from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse

from users.forms import ProfileForm


# Create your views here.


def profile_view(request, pk=None):
    if pk is not None:
        profile = get_object_or_404(User, id=pk).profile
    else:
        try:
            profile = request.user.profile
        except:
            raise Http404()

    context = {"profile": profile}

    return render(request, "users/profile.html", context)


@login_required
def profile_edit(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    context = {"profile": profile, "form": form}

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        print("Recieved POST request", request.FILES)
        if form.is_valid():
            print("Form is valid")
            form.save()
            return redirect("profile-view")

    if request.path == reverse("profile-onboarding"):
        template = "users/profile_onboarding.html"
    else:
        template = "users/profile_edit.html"
    return render(request, template, context)


@login_required
def profile_delete(request):
    user = request.user

    if request.method == "POST":
        logout(request)
        user.delete()
        messages.success(request, "You have successfully deleted your profile")
        return redirect("home_view")

    return render(request, "users/profile-delete.html")
