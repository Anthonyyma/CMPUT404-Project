from django.contrib import auth, messages
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView

from .forms import PostForm
from .models import Follow, FollowRequest, Post


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


def friends(request):
    users = auth.get_user_model().objects.all().values()
    friends = Follow.objects.get(followee=request.user)
    friendRequest = FollowRequest()
    data = {'users': users, 'friends': friends}
    return render(request, "friends.html", data)
