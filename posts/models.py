import uuid

from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255, null=True, blank=True)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts"
    )
    url = models.URLField(max_length=255, null=True, blank=True)
    image = models.URLField(max_length=255, blank=True, null=True)
    tags = models.ManyToManyField("Tag", blank=True, null=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created"]


class Tag(models.Model):
    name = models.CharField(max_length=25)
    image = models.FileField(upload_to="icons/", null=True, blank=True)
    slug = models.SlugField(max_length=25, unique=True)
    order = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order"]
