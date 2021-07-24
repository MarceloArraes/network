
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("posts", views.post, name="post"),
    path("likes", views.likes, name="likes"),
    path("showposts", views.showPosts, name="showposts"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("allposts", views.allposts, name="allposts"),
    path("register", views.register, name="register"),
    path("follow", views.follow_user, name="follow"),
    path("userlist", views.listUsers, name="userlist"),
    path("listUsersPage", views.listUsersPage, name="listUsersPage"),
    path("profile/<int:user_id>", views.profileUser, name="profile"),
    path("profilePage", views.profilePage, name="profilePage"),
]
