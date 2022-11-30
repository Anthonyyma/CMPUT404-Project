from core import client
from core.authors.serializers import AuthorSerializer
from core.drf_utils import CustomPagination, labelled_pagination
from core.models import Follow, FollowRequest, Like, User
from core.path_utils import get_author_id_from_url
from core.posts.serializers import LikeSerializer
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.conf import settings


class AuthorViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = User.objects.order_by("id").all()
    serializer_class = AuthorSerializer
    pagination_class = labelled_pagination("authors")

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if request.user != self.get_object():
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return self.partial_update(request, *args, **kwargs)

    @action(detail=True)
    def followers(self, request, pk=None):
        user = self.get_object()
        followers = User.objects.filter(following__followee=user)
        data = AuthorSerializer(followers, many=True, context={"request": request}).data
        paginator = CustomPagination()
        return paginator.get_paginated_response(data, type="followers")

    @action(detail=True, methods=["get"])
    def likes(self, request, **kwargs):
        user = self.get_object()
        queryset = Like.objects.order_by("-published").filter(user=user)
        data = LikeSerializer(queryset, many=True, context={"request": request}).data
        paginator = CustomPagination()
        return paginator.get_paginated_response(data, type="like")


@api_view(["GET", "PUT", "DELETE"])
def follow_view(request, author1: str = "", author2: str = ""):
    """
    GET: Checks if author2 is following author1
    PUT: Adds author2 as a follower of author1
    """
    is_following = Follow.objects.filter(follower=author2, followee=author1).exists()
    if request.method == "GET":
        if is_following:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method == "PUT":
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if str(request.user.id) != author1:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        is_following = Follow.objects.filter(
            follower=author2, followee=author1
        ).exists()
        if not is_following:
            Follow.objects.create(follower_id=author2, followee_id=author1).save()
            FollowRequest.objects.filter(
                follower_id=author2, followee_id=author1
            ).delete()
        return Response(status=status.HTTP_201_CREATED)

    elif request.method == "DELETE":
        if is_following:
            Follow.objects.filter(follower=author2, followee=author1).delete()
        return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def follow_request_view(request):
    follower_url = request.data.get("follower_url")
    followee_url = request.data.get("followee_url")
    follower_id = get_author_id_from_url(follower_url)
    followee_id = get_author_id_from_url(followee_url)

    follower = User.objects.filter(id=follower_id).first()
    followee = User.objects.filter(id=followee_id).first()
    if settings.API_HOST_PATH in followee_url:
        FollowRequest.objects.create(follower=follower, followee=followee)
        return Response(
            "Created follow request locally", status=status.HTTP_201_CREATED
        )

    resp = client.send_external_follow_request(follower, followee_url, request)
    return Response(resp.json(), status=resp.status_code)
