from django.shortcuts import render, redirect

from users.forms import ProfileForm


# Create your views here.


def profile_view(request):
    profile = request.user.profile
    context = {"profile": profile}
    return render(request, "users/profile.html", context)


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
    return render(request, "users/profile_edit.html", context)
