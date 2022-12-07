from core import client
from core.models import Follow, FollowRequest, Post, User
from core.path_utils import get_author_id_from_url, get_author_url
from core.posts.serializers import PostSerializer
from django.conf import settings
from django.shortcuts import render


def all_users_view(request):
    client.sync_external_authors()

    all_users = User.objects.order_by("username")
    context = {"users": all_users}
    return render(request, "allUsers.html", context)


def user_detail(request):
    context = {"ownProfile": False}
    user = None
    if "url" in request.GET:
        url = request.GET["url"]
        if settings.API_HOST_PATH in url:
            id = get_author_id_from_url(url)
            user = User.objects.get(id=id)
        else:
            user_data = client.fetch_external_user(url)
            client.create_update_external_authors(user_data)
            user = User.objects.get(external_url=url)
    elif "id" in request.GET:
        user = User.objects.get(id=request.GET["id"])
    else:
        user = request.user
        context["ownProfile"] = True

    posts = []
    if user.external_url is None:
        posts_query = Post.objects.filter(author=user).order_by("-published")
        posts = PostSerializer(
            posts_query, many=True, context={"request": request}
        ).data
    else:
        posts = client.fetch_posts_from_external_author(user)

    context = {
        "user": user,
        "posts": posts,
        "requestUserURL": get_author_url(request.user),
        "userURL": get_author_url(user),
    }
    

    context["following"] = Follow.objects.filter(
        follower=request.user, followee=user
    ).exists()  # is the user being viewed followed by the current user
    # is the user being viewed the current user
    if user == request.user:
        context["ownProfile"] = True
        follow_requests = FollowRequest.objects.filter(followee=user)
        context["follow_requests"] = follow_requests
    else:
        context["ownProfile"] = False
    context["user"] = user
    context["posts"] = posts
    print(context)
    return render(request, "viewUser.html", context)
