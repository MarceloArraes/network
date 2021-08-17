import json
from typing import ContextManager
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Likes, Post, User


def index(request):
    return render(request, "network/index.html")


def allposts(request):
    return render(request, "network/allPosts.html")


@login_required
def showposts_liked(request):
    return render(request, "network/postsLiked.html")


@login_required
def followingPage(request):
    return render(request, "network/following.html")


def profilePage(request, user_id):
    return render(request, "network/profile.html", {
        "user_id": user_id,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@csrf_exempt
@login_required
def likes(request):
    print("entered here")
    # Composing a post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)

    # print(data)
    postId = data.get("post")
    # print(postId)

# getting the post that we want to like
    posting = Post.objects.get(id=postId)
# getting the user that is liking the post
    userr = User.objects.get(id=request.user.id)

# adding to the post the usar that liked
# here we see if the post was already liked by the user (!!!!)
    try:
        userLikedResult = posting.userliked.get(id=userr.id)
        print(userLikedResult)
        posting.userliked.remove(userLikedResult)
        posting.howManylikes = posting.howManylikes - 1
        posting.save()
        print(posting.howManylikes)
        return JsonResponse({"message": "Like retrieved successfully."}, status=201)
    except ObjectDoesNotExist:
        posting.userliked.add(userr)
        posting.save()
        posting.howManylikes = posting.howManylikes + 1
        print(posting.howManylikes)
        posting.save()
        return JsonResponse({"message": "Like sent successfully."}, status=201)


@csrf_exempt
@login_required
def post(request):
    print("entered here")
    # Composing a post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check post content
    data = json.loads(request.body)
    postcontent = data.get("content", "")

    print(len(postcontent))
    if str(len(postcontent)) == '0':
        return JsonResponse({"error": "Content needed."}, status=400)
    # Get time of creation of post

# crete post and add to datebase
    posting = Post(
        postuser=request.user,
        content=postcontent,
    )
    posting.save()
    return JsonResponse({"message": "Post sent successfully."}, status=201)


@login_required
def follow_user(request, user_id):
    print("ENTROU EM FOLLOW! !!!!!!!!!!!!!!")
    userr = User.objects.get(id=request.user.id)
    userToFollow = User.objects.get(id=user_id)
    userr.following1.add(userToFollow)
    userr.save()
    userToFollow.followers += 1
    userToFollow.save()

    return JsonResponse({"message": "User Followed sucessfully"}, status=201)


@login_required
def unfollow_user(request, user_id):
    print("ENTROU EM UNFOLLOW! !!!!!!!!!!!!!!")
    userr = User.objects.get(id=request.user.id)
    userToFollow = User.objects.get(id=user_id)
    userr.following1.remove(userToFollow)
    userr.save()
    userToFollow.followers -= 1
    userToFollow.save()

    return JsonResponse({"message": "User Unfollowed sucessfully"}, status=201)


@login_required
def followingList(request):
    posts = []
    userr = User.objects.get(id=request.user.id)
    followings = userr.following1.all()

    for follow in followings:
        posts.extend(list(Post.objects.filter(
            postuser=follow).all()))

    posts.sort(key=lambda x: x.id, reverse=True)

    return JsonResponse([post.serialize() for post in posts], safe=False)
    return False


def showPosts(request):
    posts = Post.objects.all()
    # Return posts in reverse chronologial order
    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)
    return False


@csrf_exempt
def editPost(request):
    print("Entered editPost")

    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    postid = data.get("post_id", "")
    postContent = data.get("content", "")

    post = Post.objects.get(pk=postid)
    print(post.content)
    print(postContent)
    post.content = postContent
    post.save()

    print([post.serialize()])

    return JsonResponse([post.serialize()], safe=False)


@login_required
def showPostsLiked(request):
    posts = Post.objects.filter(userliked=request.user)
    #posts = Post.objects.all()
    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)
    return False


@csrf_exempt
@login_required
def showPostsProfile(request):
    print("Entered SHOWPOSTSPROFILE")
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    print("Entered SHOWPOSTSPROFILE POST")
    user_id = data.get("userProfile")
    userr = User.objects.get(pk=user_id)

    posts = Post.objects.filter(postuser=userr)
    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)

    return False


def listUsersPage(request):
    return render(request, "network/userlists.html")


def listUsers(request):
    users = User.objects.all()
    return JsonResponse([user.serialize() for user in users], safe=False)
    return False


@csrf_exempt
def profileUser(request, user_id):
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)

    if (request.method == 'GET'):
        if user_id == None:
            return JsonResponse({"error": "Profile needed."}, status=400)

        users = User.objects.get(id=user_id)

        return JsonResponse([users.serialize()], safe=False)
        # return JsonResponse({"message": "Post sent successfully."}, status=201)
    return JsonResponse({"error": "GET request required."}, status=400)
