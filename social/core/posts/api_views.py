from core.drf_utils import labelled_pagination
from core.models import Post, Comment
from core.posts.serializers import PostSerializer, CommentSerializer
from rest_framework import viewsets


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.order_by("id").all()
    serializer_class = PostSerializer
    pagination_class = labelled_pagination("post")

    def get_queryset(self):
        queryset = Post.objects.order_by("published").all()
        # This comes from the nested router
        # /api/authors/<author_pk>/posts/
        author_id = self.kwargs["author_pk"]
        queryset = queryset.filter(author=author_id)
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.order_by("id").all()
    serializer_class = CommentSerializer
    pagination_class = labelled_pagination("comment")

    def get_queryset(self):
        queryset = Comment.objects.order_by("published").all()
        # This comes from the nested router
        # /api/authors/<author_pk>/posts/<post_pk>/comments/
        post_id = self.kwargs["post_pk"]
        queryset = queryset.filter(post=post_id)
        return queryset
