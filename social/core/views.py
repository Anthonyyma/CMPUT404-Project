from django.shortcuts import HttpResponseRedirect, get_object_or_404, render, redirect
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from .forms import PostForm, CommentForm
from .models import Post, User, Like, Comment
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView
from django.contrib import messages
import markdown
from html.parser import HTMLParser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse


class PostList(LoginRequiredMixin, ListView):
    login_url = "/login/"
    template_name = "myPosts.html"
    model = Post

    def get_queryset(self):
        queryset = super(PostList, self).get_queryset()
        return queryset.filter(author=self.request.user)

class MDParser(HTMLParser):
    md = ""
    def handle_data(self, data):
        self.md += data

# @login_required
def createPost(request):
    list(messages.get_messages(request))
    form = PostForm(request.POST or None, request.FILES or None)
    postId = request.GET.get('id')
    type = request.GET.get('type')
    notValid = False
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
                data = markdown.markdown(form.instance.content)
                parser = MDParser()
                parser.feed(data)
                form.instance.content = parser.md
            if not notValid:
                form.save()
                return redirect("/")
        else:
            print(form.errors)

    context = {'form': form, 'type':type, 'id':postId}
    return render(request, "createPost.html", context)

# incomplete
def likePost(request, postID):
    form = Like(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = postID

    return HttpResponseRedirect(reverse('postContent', args=[postID]))

# @login_required
def createComment(request):
    list(messages.get_messages(request))
    form = CommentForm(request.POST or None)
    commentId = request.GET.get('post.id')
    print(commentId)
    if commentId != None:
        comment = Comment.objects.get(id=commentId)
        form = CommentForm(instance=comment)

    if request.method == "POST":
        if commentId != None:
            form = CommentForm(request.POST, instance=comment)
        else:
            form = CommentForm(request.POST)
        print(form.is_valid)
        if form.is_valid():
            form.instance.author = request.user
        else:
            print(form.errors)


    context = {'form': form, 'id':commentId}
    return render(request, "postContent/createComment.html", context)

# @login_required
def deletePost(request):
    postId = request.GET.get('id')
    if postId != "None":
        Post.objects.filter(pk=postId).delete()
    return redirect("/")

# @login_required
def postType(request):
    return render(request, "postType.html")

def postContent(request):
    postId = request.GET.get('id')
    post = Post.objects.get(id=postId)
    user = request.user
    ownPost = False
    if user == post.author:
        ownPost = True
    if post:
        profilePic = user.profile_image
    
    context = {'post':post, 'ownPost':ownPost, 'profilePic': profilePic, 'username': user.username, 'content': post.content, 'img': post.image}
    return render(request, "postContent/postContent.html", context)

def viewUser(request, userID):
    # Displays the information of a user
    # User has both custom fields and base fields (see models.py)

    if (userID is None):    #if a userID is not given default to current user
        userID = request.user.id    # Currently logged in user

    user = User.objects.get(id=userID)  #this should get the user from the database
    
    context = {"user":user}     # send the user to the template
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

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been succefully logged out"))
    return redirect('login')

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
