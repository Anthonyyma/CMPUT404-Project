from core.authors.serializers import AuthorSerializer
from core.drf_utils import get_api_root_url
from core.models import Comment, Post
from rest_framework import serializers


def get_post_url(post: Post, request) -> str:
    """
    Returns the api url for a post
    """
    return f"{get_api_root_url(request)}authors/{post.author.id}/posts/{post.id}/"


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    comment = serializers.CharField(source="content")
    contentType = serializers.CharField(source="content_type", default="text/markdown")
    type = serializers.ReadOnlyField(default="comment")
    id = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "type",
            "author",
            "comment",
            "contentType",
            "published",
            "comment",
            "id",
        )

    def get_id(self, obj: Comment):
        return get_post_url(obj.post, self.context["request"]) + f"comments/{obj.id}/"


class PostSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default="post")
    contentType = serializers.CharField(source="content_type")
    # comments = serializers.HyperlinkedRelatedField()
    visibility = serializers.SerializerMethodField()
    author = AuthorSerializer()
    categories = serializers.SerializerMethodField()
    author = AuthorSerializer(read_only=True)
    published = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    commentsSrc = serializers.SerializerMethodField()

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
            "commentsSrc",
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

    def get_id(self, obj: Post):
        return get_post_url(obj, self.context["request"])

    def get_comments(self, obj: Post):
        return get_post_url(obj, self.context["request"]) + "comments/"

    def get_commentsSrc(self, obj: Post):
        recent_comments = obj.comments.order_by("-published")[:5]
        comment_serializer = CommentSerializer(
            recent_comments, many=True, context=self.context
        )
        return {
            "type": "comments",
            "page": 1,
            "size": recent_comments.count(),
            "post": get_post_url(obj, self.context["request"]),
            "id": get_post_url(obj, self.context["request"]) + "comments/",
            "comments": comment_serializer.data,
        }
