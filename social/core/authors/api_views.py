from core.authors.serializers import AuthorSerializer
from core.models import User
from core.pagination import CustomPagination, labelled_pagination
from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action


class AuthorViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = User.objects.order_by("id").all()
    serializer_class = AuthorSerializer
    permission_class = [permissions.AllowAny]
    pagination_class = labelled_pagination("authors")

    def post(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @action(detail=True)
    def followers(self, request, pk=None):
        user = self.get_object()
        followers = User.objects.filter(following__followee=user)
        data = AuthorSerializer(followers, many=True, context={"request": request}).data
        paginator = CustomPagination()
        return paginator.get_paginated_response(data, type="followers")
