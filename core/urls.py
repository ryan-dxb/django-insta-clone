"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from posts.views import (
    home_view,
    post_create_view,
    post_delete_view,
    post_edit_view,
    post_detail_view,
)
from users.views import profile_view, profile_edit, profile_delete

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", home_view, name="home_view"),
    path("category/<slug:category_slug>", home_view, name="category-view"),
    path("posts/create", post_create_view, name="post-create"),
    path("posts/delete/<pk>", post_delete_view, name="post-delete"),
    path("posts/edit/<pk>", post_edit_view, name="post-edit"),
    path("posts/<pk>", post_detail_view, name="post-detail"),
    path("profile", profile_view, name="profile-view"),
    path("profile/edit", profile_edit, name="profile-edit"),
    path("profile/delete", profile_delete, name="profile-delete"),
    path("profile/onboarding", profile_edit, name="profile-onboarding"),
    path("profile/<pk>", profile_view, name="user-profile"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
