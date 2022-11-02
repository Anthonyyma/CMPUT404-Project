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
    id = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "type",
            "id",
            "source",
            "origin",
            "contentType",
            "content",
            "author",
            "categories",
            "count",
            "comments",
            "visibility",
            "published",
            "unlisted",
        ]

    def _get_api_root_url(self) -> str:
        """
        Returns the root url of the API
        https://domain.com/api/
        """
        request = self.context["request"]
        url: str = request.build_absolute_uri()
        base_url = url.split("/api/")[0]
        return f"{base_url}/api/"

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

    def get_id(self, obj: Post):
        api_root = self._get_api_root_url()
        id = f"{api_root}/authors/{obj.author.id}/posts/{obj.id}/"
        return id

    def get_comments(self, obj: Post):
        api_root = self._get_api_root_url()
        id = f"{api_root}/authors/{obj.author.id}/posts/{obj.id}/comments/"
        return id
