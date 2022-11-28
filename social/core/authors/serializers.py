from core.models import User
from core.path_utils import get_author_url
from rest_framework import serializers
from rest_framework.request import Request


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
        if obj.external_url:
            return obj.external_url
        return get_author_url(obj)
