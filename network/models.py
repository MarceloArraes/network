from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model


class User(AbstractUser):
    pass


class Post(models.Model):
    postuser = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "user": self.postuser.username,
            "content": self.content,
            "timestamp": self.timestamp

        }
