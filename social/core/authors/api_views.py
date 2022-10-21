from core.authors.serializers import AuthorSerializer
from core.models import User
from core.pagination import CustomPagination
from rest_framework import mixins, permissions, viewsets


class AuthorViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
):
    queryset = User.objects.order_by("id").all()
    serializer_class = AuthorSerializer
    permission_class = [permissions.AllowAny]
    pagination_class = CustomPagination
