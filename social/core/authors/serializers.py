from core.models import User
from rest_framework import serializers
from rest_framework.request import Request
from core.path_utils import get_author_url


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    type = serializers.ReadOnlyField(default="author")
    host = serializers.SerializerMethodField()
    displayName = serializers.CharField(source="username")

    class Meta:
        model = User
        fields = [
            "type",
            "id",
            "url",
            "host",
            "displayName",
            "github",
            "email",
        ]
        extra_kwargs = {
            "url": {"read_only": True},
        }

    def get_host(self, obj: User) -> str:
        request: Request = self.context["request"]
        return request.get_host()

    def get_id(self, obj: User) -> str:
        return get_author_url(obj, self.context["request"])
