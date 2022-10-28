from core.authors.serializers import AuthorSerializer
from core.models import User
from core.pagination import CustomPagination, labelled_pagination
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


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
