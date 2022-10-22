from django.shortcuts import render
from .forms import PostForm
from .models import Post

def createPost(request):
    form = PostForm(request.POST or None)
    post = Post.objects.get(author=request.user)

    # form = PostForm(instance=post)
    print(post.id)

    if request.method == "POST":
        # form = PostForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
        else:
            print(form.errors)

    context = {'form': form}
    return render(request, "createPost.html", context)

def editPost(request): 
    pass
    # create object of form

    # post = Post.objects.get(author="a")
    # print(post.id)
    # form = ""
    # form = PostForm(instance=post)

    # if request.method == "POST":
    #     print(request.POST)
    #     form = PostForm(request.POST)
    #     if form.is_valid():
    #         form.save()

    # context = {'form':'a'}
    # return render(request, "editPost.html", context)
