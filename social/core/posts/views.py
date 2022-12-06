from core import client
from core.authors.serializers import AuthorSerializer
from core.models import Post
from core.path_utils import get_post_id_from_url
from core.posts.serializers import PostSerializer
from django.conf import settings
from django.shortcuts import render


def post_detail(request):
    if "url" in request.GET:
        url = request.GET["url"]
        if settings.API_HOST_PATH in url:  # check if the url contains our own address
            post = Post.objects.get(id=get_post_id_from_url(url))
            post = PostSerializer(post, context={"request": request}).data
        else:
            post = client.fetch_external_post(url)
    else:
        return 404

    own_post = str(request.user.id) in post["author"]["id"]
    user = request.user
    user_data = AuthorSerializer(user, context={"request": request}).data
    # if post:
    #     profilePic = post.author.profile_image
    #     if post.content_type == "APP64":
    #         with open("media/temp.jpg", "wb") as f:
    #             f.write(base64.b64decode(post.content))
    #             post.image = "temp.jpg"
    print(post)
    comments = client.get_comments(post["comments"])
    context = {
        "post": post,
        "own_post": own_post,
        "username": user.username,
        # "img": post.image,
        "comments": comments,
        "user": user_data,
    }
    return render(request, "postContent/postContent.html", context)