from typing import Dict

from core import path_utils
from core.authors.serializers import AuthorSerializer
from core.models import Comment, Follow, FollowRequest, Inbox, Like, Post, User
from core.posts.serializers import LikeSerializer
from django.conf import settings
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

API_HOST_PATH = settings.API_HOST_PATH


class InboxView(APIView):
    """
    This view handles posts, follow requests, like and comments.
    GET: Returns the inbox for the current user
    """

    def post(self, request: Request, recipient_id: str = "", **kwargs):
        recipient = User.objects.get(id=recipient_id)
        data = request.data
        if data is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        type = data.get("type").lower()
        if type == "like":
            return self.handle_like(data)
        elif type == "post":
            return self.handle_post(data, recipient)
        elif type == "follow":
            return self.handle_follow(data, recipient)

    def handle_like(self, data):
        like = Like()
        if API_HOST_PATH in data["author"]["id"]:  # liker is local
            liker_id = path_utils.get_author_id_from_url(data["author"]["id"])
            liker = User.objects.get(id=liker_id)
            like.user = liker
        else:  # liker is external
            like.external_user = data["author"]["id"]

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

    def handle_post(self, data, recipient: User):
        post_url = data["id"]
        inbox = Inbox(user=recipient, external_post=post_url)
        inbox.save()
        return Response(status=status.HTTP_201_CREATED)

    def handle_follow(self, data, recipient: User):
        follower_url = data["actor"]["id"]
        follower = self.create_update_external_user(data["actor"])
        already_following = Follow.objects.filter(
            followee=recipient, external_follower=follower_url
        ).exists()
        already_requested = FollowRequest.objects.filter(
            followee=recipient, external_follower=follower_url
        )
        if already_following or already_requested:
            return Response(status=status.HTTP_200_OK)

        follow_request = FollowRequest(
            followee=recipient, external_follower=follower_url, follower=follower
        )
        follow_request.save()
        return Response(status=status.HTTP_201_CREATED)

    def handle_comment(self, data):
        author_url = data["author"]["id"]
        post_url = data["post"]
        if API_HOST_PATH not in post_url:
            return Response(
                "You can only submit comments for posts on this node",
                status=status.HTTP_400_BAD_REQUEST,
            )
        post_id = path_utils.get_post_id_from_url(post_url)
        post = Post.objects.filter(id=post_id).first()
        if not post:
            return Response("Post does not exist", status=status.HTTP_404_NOT_FOUND)
        comment = Comment(
            content=data["content"],
            external_author=author_url,
            content_type=data.get("contentType", "text/markdown"),
            post=post,
        )
        comment.save()

    def create_update_external_user(self, author_data: Dict) -> User:
        serializer = AuthorSerializer(data=author_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return serializer.save(external_url=author_data["id"])
