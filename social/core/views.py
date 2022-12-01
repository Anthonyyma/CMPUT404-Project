import base64
from html.parser import HTMLParser

import markdown
import requests
from core import client
from core.posts.serializers import PostSerializer
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required  # noqa
from django.shortcuts import redirect, render

from .authors.serializers import AuthorSerializer
from .client import fetch_external_post
from .forms import EditUserForm, PostForm, RegisterForm
<<<<<<< HEAD
from .models import Follow, Inbox, Post, User
from .path_utils import (get_author_id_from_url, get_author_url,
                         get_post_id_from_url)

=======
from .models import Follow, Inbox, Post, User, FollowRequest
from .path_utils import get_author_url, get_post_id_from_url
from django.conf import settings
>>>>>>> eef8af2f40c721a5fc8dba45040d5bcc2e082647

@login_required
def showFeed(request):
    # My own posts

    posts = Post.objects.filter(author=request.user)
    srlizedPost = PostSerializer(posts, many=True, context={'request': request}).data

    internPosts = Post.objects.filter(inbox__user=request.user)
    srlizedPost = srlizedPost + PostSerializer(
        internPosts, many=True, context={'request': request}).data

    externPosts = Inbox.objects.filter(user=request.user).exclude(
        external_post__isnull=True)
    for externPost in externPosts:
        srlizedPost.append(fetch_external_post(externPost.external_post))

    return render(request, "feed.html", {"posts": srlizedPost})


def publicFeed(request):
    posts = Post.objects.filter(
        author=request.user, friends_only=False, unlisted=False, private_to='')
    srlizedPost = PostSerializer(posts, many=True, context={'request': request}).data

    internPosts = Post.objects.filter(inbox__user=request.user)
    srlizedPost = srlizedPost + PostSerializer(
        internPosts, many=True, context={'request': request}).data

    externPosts = Inbox.objects.filter(user=request.user).exclude(
        external_post__isnull=True)
    for externPost in externPosts:
        srlizedPost.append(fetch_external_post(externPost.external_post))

    return render(request, "publicFeed.html", {"posts": srlizedPost})


class MDParser(HTMLParser):
    md = ""

    def handle_data(self, data):
        self.md += data

# @login_required
def createPost(request):
    list(messages.get_messages(request))
    form = PostForm(request.POST or None, request.FILES or None)
    postId = request.GET.get("id")
    postType = request.GET.get("type")
    notValid = False

    if postId is not None:
        post = Post.objects.get(id=postId)
        form = PostForm(instance=post)
        postType = form.instance.content_type

    if request.method == "POST":
        if postId is not None:
            form = PostForm(request.POST, instance=post)
        else:
            form = PostForm(
                request.POST,
                request.FILES,
            )
        if form.is_valid():
            form.instance.author = request.user
            form.instance.content_type = postType
            if postType == "PNG" or postType == "JPEG":
                if not form.instance.image:
                    messages.info(request, "No Image")
                    notValid = True
            elif postType == "MD":
                pass
            if not notValid:
                newPost = form.save()
                if len(newPost.private_to) != 0:  #if private to someone
                    user = User.objects.filter(username=newPost.private_to).first()
                    if user:
                        if user.external_url:  # if external user
                            follow = Follow.objects.filter(followee=user)
                            url = getattr(follow, "external_follower") + "inbox/"
                            msg = PostSerializer(newPost, context={'request': request}).data
                            msg["description"] = "test"
                            if "cmsjmnet" in url:
                                msg = {"items":[msg], "author":get_author_url(request.user)}
                                r = requests.post(url, json = msg, auth=("team8", "team8"))
                            else:
                                r = requests.post(url, json = msg, auth=("", ""))
                        else:
                            Inbox.objects.create(post=newPost, user=user)
                elif newPost.friends_only:
                    pass
                elif not newPost.unlisted:
                    for follow in Follow.objects.filter(followee=request.user):
                        if follow.external_follower:
                            url = getattr(follow, "external_follower") + "inbox/"
                            msg = PostSerializer(newPost, context={'request': request}).data
                            msg["description"] = "test"
                            if "cmsjmnet" in url:
                                msg = {"items":[msg], "author":get_author_url(request.user)}
                            print(msg)
                            print(type(msg))
                            r = requests.post(url, json = msg, auth=("team8", "team8"))
                            print("here:", r.status_code)
                            with open("response.html", "w") as f:
                                f.write(r.text)
                        else:
                            Inbox.objects.create(post=newPost, user=follow.follower)
                return redirect("/")
        else:
            print(form.errors)

    context = {"form": form, "type": postType, "id": postId}
    return render(request, "createPost.html", context)


# @login_required
def deletePost(request):
    postId = request.GET.get("id")
    if postId != "None":
        Post.objects.filter(pk=postId).delete()
    return redirect("/")


# @login_required
def postType(request):
    return render(request, "postType.html")


def postContent(request):
    post = None
    if 'url' in request.GET:
        url = request.GET['url']
        if settings.API_HOST_PATH in url: # check if the url contains our own address
            post = Post.objects.get(id=get_post_id_from_url(url))
        else:
            data = client.fetch_external_post(url)
            serializer = PostSerializer(data=data)
            if (serializer.is_valid()):
                post = Post(**serializer.validated_data)
    else:
        return 404

    user = request.user
    ownPost = False
    if user == post.author:
        ownPost = True
    if post:
        profilePic = post.author.profile_image
        if post.content_type == "APP64":
            with open("media/temp.jpg", "wb") as f:
                f.write(base64.b64decode(post.content))
                post.image = "temp.jpg"

    authorURL = get_author_url(post.author)
    context = {
        "post": post,
        "ownPost": ownPost,
        "profilePic": profilePic,
        "username": user.username,
        "content": post.content,
        "img": post.image,
        "authorurl": authorURL,
    }
    return render(request, "postContent/postContent.html", context)


def follower_view(request):
    user = request.user
    followers = []      # json array of followers
    for follow in Follow.objects.filter(followee=user):
        """
        if follow.external_follower is not None:
            data = request.get(follow.external_follower).data
        else:
            data = AuthorSerializer(request, follow.follower).data
        followers.append(data)
        """
        followers.append(follow.follower)

    context = {'followers': followers, 'request': request}
    return render(request, "followers.html", context)


def following_view(request):
    user = request.user
    following = []      # json array of following
    for follow in Follow.objects.filter(follower=user):
        """
        if follow.external_follower is not None:
            data = request.get(follow.external_follower).data
        else:
            data = AuthorSerializer(request, follow.follower).data
        following.append(data)
        """
        following.append(follow.followee)


    context = {'following': following, 'request': request}
    return render(request, "following.html", context)


def all_users_view(request):
    all_users = User.objects.all()
    context = {'users': all_users}
    return render(request, "all_users.html", context)


def viewUser(request, userID):
    # Displays the information of a user
    # User has both custom fields and base fields (see models.py)

    if userID is None:  # if a userID is not given default to current user
        userID = request.user.id  # Currently logged in user

    if 'url' in request.GET:
        url = request.GET['url']
<<<<<<< HEAD
        if settings.API_HOST_PATH in url: # check if the url contains our own address
            user = User.objects.get(id=get_author_id_from_url(url))  # this should get the user from the database
=======
        data = client.fetch_external_user(url)
        existing = User.objects.filter(external_url=url).first()
        serializer = AuthorSerializer(existing, data=data)
        if serializer.is_valid() and existing is None:
            user = serializer.save(external_url=url)
>>>>>>> eef8af2f40c721a5fc8dba45040d5bcc2e082647
        else:
            data = client.fetch_external_user(url)
            existing = User.objects.filter(external_url=url).first()
            serializer = AuthorSerializer(existing, data=data)
            if serializer.is_valid():
                user = serializer.save(external_url=url)
            else:
                return 404
    else: 
        user = User.objects.get(id=userID)

    """
    if user.external_user is not None:
        data = request.get(user.external_user).data
        user = User(**data) #add the data to the user (not sure if this is permanent)
    """
    # send the user to the template
    context = {"user": user, "userURL": get_author_url(user),
               "requestUserURL": get_author_url(request.user)}

    if user.external_url is not None:
        context["userURL"] = user.external_url

    if (request.user == user):     # if the user is viewing their own profile
        context["ownProfile"] = True
        follow_requests = FollowRequest.objects.filter(followee=user)
        context["follow_requests"] = follow_requests
    else:
        context["ownProfile"] = False
        # check if the current user is following the user
        if (Follow.objects.filter(follower=request.user, followee=user).exists()):
            context["following"] = True
        else:
            context["following"] = False

    posts = Post.objects.filter(author=user)
    context["posts"] = posts

    return render(request, "viewUser.html", context)


def viewCurrentUser(request):
    userID = request.user.id
    return viewUser(request, userID)


def editUser(request):
    """
    editUser function to provide a form for users to edit their profile

    if POST request:
        pass the form to display

        check if the filled form is valid

    return:
        editUser form
    """
    # if the method is POST
    if request.method == "POST":
        # pass the request's body to the registeration form
        form = EditUserForm(request.POST, request.FILES, instance=request.user)
        # if the data is valid, save user in databse and redirect to homepage
        if form.is_valid():
            form.save()
            # once registered redirect to a different page
            return redirect("viewCurrentUser")
    else:
        form = EditUserForm(instance=request.user)
    # render the registeration html template
    return render(request, "editUser.html", {"form": form})


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("feed")
        else:
            messages.success(
                request,
                ("Please double check that you are using the correct username and password"),   # noqa
            )
            return redirect("login")
    else:
        return render(request, "registration/login.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been succefully logged out"))
    return redirect("login")


def register_user(request):
    """
    registration function to provide a form for users to create an accout on

    if POST request:
        pass the form to display

        check if the filled form is valid

    return:
        registration form
    """
    # if the method is POST
    if request.method == "POST":
        # pass the request's body to the registeration form
        form = RegisterForm(request.POST)
        # if the data is valid, save user in databse and redirect to homepage
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect("myPosts")  # once registered redirect to a different page
    else:
        form = RegisterForm()
    # render the registeration html template
    return render(request, "registration/register.html", {"form": form})
