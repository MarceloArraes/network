
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("posts", views.post, name="post"),
    path("showposts", views.showPosts, name="showposts"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("follow", views.follow_user, name="follow"),
    path("userlist", views.listUsers, name="userlist"),
]
