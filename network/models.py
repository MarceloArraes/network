from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model


class User(AbstractUser):
    following1 = models.ManyToManyField("self", symmetrical=False)

    def serialize(self):
        return {
            "user_id": self.id,
            "user": self.username,
            "email": self.email,
            "date_joined": self.date_joined,
            "superuser": self.is_superuser,
        }

    pass


class Post(models.Model):
    postuser = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)

    def serialize(self):
        return {
            "user": self.postuser.username,
            "content": self.content,
            "timestamp": self.timestamp,
            "likes": self.likes,
            "id": self.id,
        }
