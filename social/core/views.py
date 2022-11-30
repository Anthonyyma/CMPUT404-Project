import base64
from html.parser import HTMLParser

import markdown
import requests
from core.posts.serializers import PostSerializer
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required  # noqa
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import ListView

from .feed.client import getExternPost
from .forms import EditUserForm, PostForm, RegisterForm
from .models import Follow, Inbox, Post, User


# @login_required
class PostList(LoginRequiredMixin, ListView):
    login_url = "/login/"
    template_name = "feed.html"
    model = Inbox

    def parseExtData(self) -> dict:
        data: Inbox = super(PostList, self).get_queryset().filter(user=self.request.user)
        postData = {}
        for post in data:
            if (post.values()["post"] is None):
                # Get post from the external server
                postData = getExternPost(post.values()["external_post"])
            else:
                postData = post.values()["post"].values()

        return postData


    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)

        # serialize the data (json)

        context["my_post_list"] = Post.objects.filter(author=self.request.user)
        context["friend_post_list"] = self.parseExtData()
        return context

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
            elif postType == "APP64":
                uploadedFile = request.FILES["image"].read()
                form.instance.content = base64.b64encode(uploadedFile).decode("ascii")
            elif postType == "MD":
                data = markdown.markdown(form.instance.content)
                parser = MDParser()
                parser.feed(data)
                form.instance.content = parser.md
            if not notValid:
                newPost = form.save()
                for follow in Follow.objects.filter(followee=request.user):
                    if follow.external_follower:
                        url = request.user.external_url + "/inbox/"
                        msg = PostSerializer(newPost).data
                        requests.post(url, json = msg)
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
    postId = request.GET.get("id")
    post = Post.objects.get(id=postId)
    user = request.user
    ownPost = False
    if user == post.author:
        ownPost = True
    if post:
        profilePic = user.profile_image
        if post.content_type == "APP64":
            with open("media/temp.jpg", "wb") as f:
                f.write(base64.decodebytes(post.content.encode()))
            post.image = "temp.jpg"

    context = {
        "post": post,
        "ownPost": ownPost,
        "profilePic": profilePic,
        "username": user.username,
        "content": post.content,
        "img": post.image,
    }
    return render(request, "postContent/postContent.html", context)


def viewUser(request, userID):
    # Displays the information of a user
    # User has both custom fields and base fields (see models.py)

    if userID is None:  # if a userID is not given default to current user
        userID = request.user.id  # Currently logged in user

    user = User.objects.get(id=userID)  # this should get the user from the database

    context = {"user": user}  # send the user to the template
    print(userID)

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
            return redirect('feed')
        else:
            messages.success(
                request,
                (
                    "Please double check that you are using the correct username and password"
                ),
            )  # noqa
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
