from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model


class User(AbstractUser):
    following1 = models.ManyToManyField("self", symmetrical=False)
    followers = models.PositiveIntegerField(default=0)

    def serialize(self):
        return {
            "user_id": self.id,
            "user": self.username,
            "email": self.email,
            "date_joined": self.date_joined.strftime("%d-%m-%Y %H:%M"),
            "superuser": self.is_superuser,
            "following": int(self.following1.count()),
            "followers": self.followers,
        }


class Likes(models.Model):
    userliked = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="userlikes")
    postliked = models.ForeignKey(
        "Post", on_delete=models.CASCADE, related_name="postliked")

    def serialize(self):
        return {
            "user": self.userliked,
            "post": self.postliked
        }


class Post(models.Model):
    postuser = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    howManylikes = models.PositiveIntegerField(default=0)
    editMode = models.BooleanField(default=False)

    userliked = models.ManyToManyField("User", through='Likes')

    def serialize(self):
        return {
            "user": self.postuser.username,
            "user_id": self.postuser.id,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%d-%m-%Y %H:%M"),
            "likes": self.howManylikes,
            "id": self.id,
            "editMode": self.editMode,
        }
