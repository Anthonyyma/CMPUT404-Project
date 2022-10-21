from core.models import User
from rest_framework import serializers
from rest_framework.request import Request


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    type = serializers.ReadOnlyField(default="author")
    host = serializers.SerializerMethodField()
    displayName = serializers.CharField(source="username")
    github = serializers.CharField(source="github_url")

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
