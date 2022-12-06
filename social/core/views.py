import base64
from html.parser import HTMLParser

import requests
from core.posts.serializers import PostSerializer
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required  # noqa
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .client import fetch_external_post
from .forms import EditUserForm, PostForm, RegisterForm
from .models import Follow, Inbox, Post, User
from .path_utils import get_author_url, get_post_id_from_url


class ImagePostView(APIView):
    def get(self, request, author_id, post_id):
        try:
            post = Post.objects.get(id=post_id, author_id=author_id)
            if "image" not in post.content_type:
                return Response(
                    {"message": "Post is not an image post"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Known issue: Remote followers cannot view friends-only image posts
            # because this is an architectural limitation
            # that is caused by a BS project specification
            # (polling based system vs webhooks)
            unauthorized = (
                post.visibility != "PUBLIC"
                and post.author.id != request.user.id
                and Follow.objects.filter(
                    follower=request.user.id, followee=post.author.id
                ).count()
                == 0
            )
            if unauthorized:
                return Response(
                    {"message": "You are not authorized to view this post"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            response_content_type = post.content_type.split(";")[0]
            image = base64.b64decode(post.content.strip("b'").strip("'"))
            return Response(
                image, content_type=response_content_type, status=status.HTTP_200_OK
            )
        except Post.DoesNotExist:
            # TODO: might exist remotely
            return Response(
                {"message": "Image post not found"}, status=status.HTTP_404_NOT_FOUND
            )


@login_required
def showFeed(request):
    # My own posts

    posts = Post.objects.filter(author=request.user)
    srlizedPost = PostSerializer(posts, many=True, context={"request": request}).data

    internPosts = Post.objects.filter(inbox__user=request.user)
    srlizedPost = (
        srlizedPost
        + PostSerializer(internPosts, many=True, context={"request": request}).data
    )

    externPosts = Inbox.objects.filter(user=request.user).exclude(
        external_post__isnull=True
    )
    for externPost in externPosts:
        srlizedPost.append(fetch_external_post(externPost.external_post))

    return render(request, "feed.html", {"posts": srlizedPost})


def publicFeed(request):
    posts = Post.objects.filter(friends_only=False, unlisted=False, private_to="")
    srlizedPost = PostSerializer(posts, many=True, context={"request": request}).data

    internPosts = Post.objects.filter(inbox__user=request.user)
    srlizedPost = (
        srlizedPost
        + PostSerializer(internPosts, many=True, context={"request": request}).data
    )

    externPosts = Inbox.objects.filter(user=request.user).exclude(
        external_post__isnull=True
    )
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

    # check if id has url and get id if it does
    if settings.API_HOST_PATH in postId:
        postId = get_post_id_from_url(postId)

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
            # if postType == "PNG" or postType == "JPEG":
            if postType == "PNG":
                if not form.instance.image:
                    messages.info(request, "No Image")
                    notValid = True
            elif postType == "MD":
                pass
            if not notValid:
                newPost = form.save()
                # convert to b64
                with open(form.instance.image.url[1:], "rb") as image_file:
                    newPost.content = base64.b64encode(image_file.read()).decode()
                    newPost.save()

                if len(newPost.private_to) != 0:  # if private to someone
                    user = User.objects.filter(username=newPost.private_to).first()
                    if user:
                        if user.external_url:  # if external user
                            follow = Follow.objects.filter(followee=user)
                            url = getattr(follow, "external_follower") + "inbox/"
                            msg = PostSerializer(
                                newPost, context={"request": request}
                            ).data
                            msg["description"] = "test"
                            if "cmsjmnet" in url:
                                msg = {
                                    "items": [msg],
                                    "author": get_author_url(request.user),
                                }
                                requests.post(url, json=msg, auth=("team8", "team8"))
                            else:
                                requests.post(url, json=msg, auth=("", ""))
                        else:
                            Inbox.objects.create(post=newPost, user=user)
                elif not newPost.unlisted:
                    for follow in Follow.objects.filter(followee=request.user):
                        if follow.external_follower:
                            url = getattr(follow, "external_follower") + "inbox/"
                            msg = PostSerializer(
                                newPost, context={"request": request}
                            ).data
                            msg["description"] = "test"
                            if "cmsjmnet" in url:
                                msg = {
                                    "items": [msg],
                                    "author": get_author_url(request.user),
                                }
                            requests.post(url, json=msg, auth=("team8", "team8"))
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


def follower_view(request):
    user = request.user
    followers = []  # json array of followers
    for follow in Follow.objects.filter(followee=user):
        """
        if follow.external_follower is not None:
            data = request.get(follow.external_follower).data
        else:
            data = AuthorSerializer(request, follow.follower).data
        followers.append(data)
        """
        followers.append(follow.follower)

    context = {"followers": followers, "request": request}
    return render(request, "followers.html", context)


def following_view(request):
    user = request.user
    following = []  # json array of following
    for follow in Follow.objects.filter(follower=user):
        """
        if follow.external_follower is not None:
            data = request.get(follow.external_follower).data
        else:
            data = AuthorSerializer(request, follow.follower).data
        following.append(data)
        """
        following.append(follow.followee)

    context = {"following": following, "request": request}
    return render(request, "following.html", context)


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
                (
                    "Please double check that you are using the correct username and password"  # noqa
                ),
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
            return redirect("feed")  # once registered redirect to a different page
    else:
        form = RegisterForm()
    # render the registeration html template
    return render(request, "registration/register.html", {"form": form})
