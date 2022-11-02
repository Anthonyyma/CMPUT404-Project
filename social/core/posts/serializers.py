from core.authors.serializers import AuthorSerializer
from core.models import Post
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default="post")
    contentType = serializers.CharField(source="content_type")
    # comments = serializers.HyperlinkedRelatedField()
    visibility = serializers.SerializerMethodField()
    author = AuthorSerializer(read_only=True)
    categories = serializers.SerializerMethodField()
    author = AuthorSerializer(read_only=True)
    published = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "type",
            "id",
            "source",
            "origin",
            "contentType",
            "author",
            "categories",
            "count",
            # "comments",
            "visibility",
            "published",
            "unlisted",
        ]

    def get_visibility(self, obj: Post) -> str:
        if obj.friends_only:
            return "FRIENDS"
        else:
            return "PUBLIC"

    def get_categories(self, obj: Post) -> list[str]:
        raw_string = obj.categories
        return [token.strip() for token in raw_string.split(",")]

    def get_published(self, obj: Post) -> str:
        return obj.published.isoformat(timespec="seconds")

    def get_count(self, obj: Post):
        return obj.comments.count()
