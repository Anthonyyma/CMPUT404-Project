from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import authentication, permissions, status
from core.models import Like, Post, Comment, User
from django.contrib.auth.models import User
from django.conf import settings
from core import path_utils
from core.posts.serializers import LikeSerializer
import re

API_HOST_PATH = settings["API_HOST_PATH"]


class InboxView(APIView):
    """
    This view handles posts, follow requests, like and comments.
    GET: Returns the inbox for the current user
    """

    def post(self, request: Request, *args, **kwargs):
        data = request.data
        if data is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if data.get("type") == "Like":
            self.handle_like(data)

    def handle_like(self, data):
        like = Like()
        if API_HOST_PATH in data["author"]["url"]:  # liker is local
            liker_id = path_utils.get_author_id_from_url(data["author"]["id"])
            liker = User.objects.get(id=liker_id)
            like.user = liker
        else:  # liker is external
            like.external_user = data["author"]["url"]

        liked_url = data["object"]
        if "comments" in liked_url:
            comment_id = path_utils.get_comment_id_from_url(liked_url)
            like.comment = Comment.objects.get(id=comment_id)
        elif "posts" in liked_url:
            post_id = path_utils.get_post_id_from_url(liked_url)
            like.post = Post.objects.get(id=post_id)
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data="Like object must be a post or a comment",
            )

        like.save()
        serializer = LikeSerializer(like)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)
