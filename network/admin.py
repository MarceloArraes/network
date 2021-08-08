from network.models import Likes, Post, User
from django.contrib import admin

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Likes)
