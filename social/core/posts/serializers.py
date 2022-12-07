from core.authors.serializers import AuthorSerializer
from core.models import Comment, Like, Post
from core.path_utils import get_comment_url, get_post_url
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comment = serializers.CharField(source="content")
    type = serializers.ReadOnlyField(default="comment")
    id = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "type",
            "author",
            "comment",
            "published",
            "comment",
            "id",
        )

    def get_id(self, obj: Comment):
        return get_post_url(obj.post) + f"comments/{obj.id}/"


class PostSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default="post")
    title = serializers.CharField()
    contentType = serializers.CharField(source="content_type")
    visibility = serializers.SerializerMethodField()
    author = AuthorSerializer()
    categories = serializers.SerializerMethodField()
    author = AuthorSerializer(read_only=True)
    published = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    commentsSrc = serializers.SerializerMethodField()
    contentType = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "type",
            "id",
            "source",
            "origin",
            "contentType",
            "content",
            "title",
            "author",
            "categories",
            "count",
            "comments",
            "commentsSrc",
            "visibility",
            "published",
            "unlisted",
            "image",
        ]

    def get_visibility(self, obj: Post) -> str:
        if obj.friends_only:
            return "FRIENDS"
        else:
            return "PUBLIC"

    def get_categories(self, obj: Post) -> list[str]:
        raw_string = obj.categories or ""
        return [token.strip() for token in raw_string.split(",")]

    def get_published(self, obj: Post) -> str:
        return obj.published.isoformat(timespec="seconds")

    def get_count(self, obj: Post):
        return obj.comments.count()

    def get_id(self, obj: Post):
        return get_post_url(obj)

    def get_comments(self, obj: Post):
        return get_post_url(obj) + "comments/"

    def get_commentsSrc(self, obj: Post):
        recent_comments = obj.comments.order_by("-published")[:5]
        comment_serializer = CommentSerializer(
            recent_comments, many=True, context=self.context
        )
        return {
            "type": "comments",
            "page": 1,
            "size": recent_comments.count(),
            "post": get_post_url(obj),
            "id": get_post_url(obj) + "comments/",
            "comments": comment_serializer.data,
        }

    def get_image(self, obj: Post):
        if "PNG" in obj.content_type:
            return obj.image

    def get_contentType(self, obj: Post):
        return obj.get_content_type_display()


class LikeSerializer(serializers.Serializer):
    type = serializers.ReadOnlyField(default="like")
    author = AuthorSerializer(read_only=True, source="user")
    object = serializers.SerializerMethodField()
    summary = serializers.SerializerMethodField()

    class Meta:
        model = Like
        fields = ["type", "author", "object", "summary"]

    def get_object(self, like: Like):
        if like.post is not None:
            return get_post_url(like.post)
        elif like.comment is not None:
            return get_comment_url(like.comment)

    def get_summary(self, like: Like):
        type = "post" if like.post is not None else "comment"
        return f"{like.user.username} likes your {type} "
