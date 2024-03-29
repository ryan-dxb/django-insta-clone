# Generated by Django 5.0.1 on 2024-01-26 03:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0010_likedpost_post_likes"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="LikedComment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "comment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="posts.comments"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="comments",
            name="likes",
            field=models.ManyToManyField(
                blank=True,
                related_name="likedcomments",
                through="posts.LikedComment",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
