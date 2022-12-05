import base64

from core import client
from core.models import Comment, Post
from core.path_utils import get_author_url, get_post_id_from_url
from core.posts.serializers import CommentSerializer, PostSerializer
from django.conf import settings
from django.shortcuts import render


def post_detail(request):
    post = None
    if "url" in request.GET:
        url = request.GET["url"]
        if settings.API_HOST_PATH in url:  # check if the url contains our own address
            post = Post.objects.get(id=get_post_id_from_url(url))
        else:
            data = client.fetch_external_post(url)
            serializer = PostSerializer(data=data)
            if serializer.is_valid():
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
    comments = Comment.objects.filter(post=post)
    comment_data = CommentSerializer(
        comments, many=True, context={"request": request}
    ).data
    print(comment_data[0])
    context = {
        "post": post,
        "ownPost": ownPost,
        "profilePic": profilePic,
        "username": user.username,
        "content": post.content,
        "img": post.image,
        "authorurl": authorURL,
        "comments": comment_data,
    }
    return render(request, "postContent/postContent.html", context)
