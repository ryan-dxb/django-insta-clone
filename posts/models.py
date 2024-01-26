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
    likes = models.ManyToManyField(
        User, blank=True, related_name="likedposts", through="LikedPost"
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created"]


class LikedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} : {self.post.title}"


class Tag(models.Model):
    name = models.CharField(max_length=25)
    image = models.FileField(upload_to="icons/", null=True, blank=True)
    slug = models.SlugField(max_length=25, unique=True)
    order = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order"]


class Comments(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="comments"
    )
    parent_post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    body = models.CharField(max_length=255)
    likes = models.ManyToManyField(
        User, related_name="likedcomments", blank=True, through="LikedComment"
    )
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(
        max_length=100,
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False,
    )

    class Meta:
        verbose_name_plural = "Comments"

    def __str__(self):
        try:
            return f"{self.author.username}: {self.body[:30]}"
        except:
            return f"no author : {self.body[:30]}"


class LikedComment(models.Model):
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} : {self.comment.body[:30]}"


class Reply(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="replies"
    )
    parent_comment = models.ForeignKey(
        Comments, on_delete=models.CASCADE, related_name="replies"
    )
    body = models.CharField(max_length=150)
    likes = models.ManyToManyField(
        User, related_name="likereplies", through="LikedReply"
    )
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(
        max_length=100,
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False,
    )

    def __str__(self):
        try:
            return f"{self.author.username} : {self.body[:30]}"
        except:
            return f"no author : {self.body[:30]}"

    class Meta:
        ordering = ["created"]


class LikedReply(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} : {self.reply.body[:30]}"
