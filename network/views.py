import json
from typing import ContextManager
from django.http import JsonResponse
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


def showposts_liked(request):
    return render(request, "network/postsLiked.html")


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

    print(data)
    postId = data.get("post")
    print(postId)
# crete post and add to datebase
    posting = Post.objects.get(id=postId)
    userr = User.objects.get(id=request.user.id)

    posting.userliked.add(userr)
    posting.save()

    # aqui estamos pegando todos os posts curtidos por userr
    #dekil = Post.objects.get(userliked=userr)
    # print(dekil.postuser)

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
    #postuser1 = data.get("postuser", "")
    postcontent = data.get("content", "")

    print(len(postcontent))
    if str(len(postcontent)) == '0':
        return JsonResponse({"error": "Content needed."}, status=400)
    # Get time of creation of post
    # timestamp = data.get("timestamp")


# crete post and add to datebase
    posting = Post(
        postuser=request.user,
        content=postcontent,
    )
    posting.save()
    return JsonResponse({"message": "Post sent successfully."}, status=201)


def follow_user(request):
    print(request.user.username)
    print("ENTROU EM FOLLOW! !!!!!!!!!!!!!!")
    #request.user.following1 = request.user1
    return False


def showPosts(request):
    posts = Post.objects.all()
    # Return posts in reverse chronologial order
    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)
    return False


def showPostsLiked(request):
    posts = Post.objects.filter(userliked=request.user)
    #posts = Post.objects.all()
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
    print("Entered profileUSER!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)

    if (request.method == 'GET'):
        #data = json.loads(request.body)
        #user_id = data.get("user_id1")
        if user_id == None:
            return JsonResponse({"error": "Profile needed."}, status=400)

        users = User.objects.get(id=user_id)
        return JsonResponse(users.serialize(), safe=False, status=201)
        # return JsonResponse({"message": "Post sent successfully."}, status=201)
    return JsonResponse({"error": "GET request required."}, status=400)
