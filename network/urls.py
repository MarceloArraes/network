
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("posts", views.post, name="post"),
    path("likes", views.likes, name="likes"),
    path("showposts", views.showPosts, name="showposts"),
    path("showposts/<str:page>", views.showPosts, name="showposts"),
    path("showposts_liked", views.showposts_liked, name="showposts_liked"),
    path("showpostsliked/<str:page>", views.showPostsLiked, name="showpostsliked"),
    path("showpostsliked", views.showPostsLiked, name="showpostsliked"),
    path("showPostsProfile",
         views.showPostsProfile, name="showPostsProfile"),
    path("showPostsProfile/<str:page>",
         views.showPostsProfile, name="showPostsProfile"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("allposts", views.allposts, name="allposts"),
    path("register", views.register, name="register"),
    path("follow/<int:user_id>", views.follow_user, name="follow"),
    path("unfollow/<int:user_id>", views.unfollow_user, name="unfollow"),
    path("followingPage", views.followingPage, name="followingPage"),
    path("followingList", views.followingList, name="followingList"),
    path("followingList/<str:page>", views.followingList, name="followingList"),
    path("userlist", views.listUsers, name="userlist"),
    path("editpost", views.editPost, name="editpost"),
    path("listUsersPage", views.listUsersPage, name="listUsersPage"),
    path("profile/<int:user_id>", views.profileUser, name="profile"),
    path("profilePage/<int:user_id>", views.profilePage, name="profilePage"),
]
