from django.shortcuts import render
from .forms import PostForm
from .models import Post
from django.views.generic import ListView

class PostList(ListView):
    template_name = "myPosts.html"
    model = Post

def createPost(request):
    form = PostForm(request.POST or None)
    postId = request.GET.get('id')
    if postId != None:
        post = Post.objects.get(id=postId)
        form = PostForm(instance=post)

    if request.method == "POST":
        if postId != None:
            form = PostForm(request.POST, instance=post)
        else:
            form = PostForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
        else:
            print(form.errors)

    context = {'form': form}
    return render(request, "createPost.html", context)
