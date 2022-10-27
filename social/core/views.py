from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from .forms import PostForm
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView
from django.contrib import messages


class PostList(ListView):
    template_name = "myPosts.html"
    model = Post

def test(request):
    postId = request.GET.get('id')
    post = Post.objects.get(id=postId)

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
                if form.instance.image:
                    form.save()
                    return redirect("/")
                else:
                    messages.info(request, "test")
            else:
                form.save()
                return redirect("/")
        else:
            print(form.errors)

    context = {'form': form, 'type':type}
    return render(request, "createPost.html", context)

def postType(request):
    return render(request, "postType.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('')
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
            return redirect('') # once registered redirect to a different page
        else:
            # Do something in case if form is not valid
            raise Http404
    else:
        form = RegisterForm()
    # render the registeration html template
    return render(request, "registration/register.html", {"form": form})
