from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from .forms import PostForm
from .models import Post, User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView
from django.contrib import messages
import commonmark
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class PostList(LoginRequiredMixin, ListView):
    login_url = "/login/"
    template_name = "myPosts.html"
    model = Post

    def get_queryset(self):
        queryset = super(PostList, self).get_queryset()
        return queryset.filter(author=self.request.user)

def test(request):
    postId = request.GET.get('id')
    post = Post.objects.get(id=postId)

@login_required
def createPost(request):
    list(messages.get_messages(request))
    form = PostForm(request.POST or None, request.FILES or None)
    postId = request.GET.get('id')
    type = request.GET.get('type')
    if postId != None:
        post = Post.objects.get(id=postId)
        form = PostForm(instance=post)
        type = form.instance.content_type

    if request.method == "POST":
        if postId != None:
            form = PostForm(request.POST, instance=post)
        else:
            form = PostForm(request.POST, request.FILES,)
        if form.is_valid():
            form.instance.author = request.user
            form.instance.content_type = type
            if type == "PNG" or type == "JPEG":
                if not form.instance.image:
                    messages.info(request, "No Image")
                    notValid = True
            elif type == "MD":
                parser = commonmark.Parser()
                form.instance.content = parser.parse(form.instance.content)
            if not notValid:
                form.save()
                return redirect("/")
        else:
            print(form.errors)

    context = {'form': form, 'type':type, 'id':postId}
    return render(request, "createPost.html", context)

@login_required
def deletePost(request):
    postId = request.GET.get('id')
    Post.objects.filter(pk=postId).delete()
    return redirect("/")

@login_required
def postType(request):
    return render(request, "postType.html")

def viewUser(request, userID):
    # Displays the information of a user
    # TODO: return different pages depending if it is the current user's page

    if (userID is None):    #if a userID is not given default to current user
        userID = request.user.id    # Currently logged in user

    user = User.objects.get(id=userID)  #this should get the user from the database

    context = {"user":user.username, "pfp": user.profile_image, "github": user.github}
    print(userID)

    return render(request, "viewUser.html", context)

def viewCurrentUser(request):
    userID = request.user.id
    return viewUser(request, userID)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('myPosts')
        else:
            messages.success(request, ("Please double check that you are using the correct username and password"))
            return redirect('login')
    else:
        return render(request, "registration/login.html", {})

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
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('myPosts') # once registered redirect to a different page
    else:
        form = RegisterForm()
    # render the registeration html template
    return render(request, "registration/register.html", {"form": form})
