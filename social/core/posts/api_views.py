from core.drf_utils import labelled_pagination, CustomPagination
from core.models import Post, Comment, Like
from core.posts.serializers import PostSerializer, CommentSerializer, LikeSerializer
from rest_framework import viewsets
from rest_framework.decorators import action


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.order_by("id").all()
    serializer_class = PostSerializer
    pagination_class = labelled_pagination("post")

    def put(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # we need to manually pull out the author id
        author_id = self.request.data["author"]
        serializer.save(author_id=author_id)

    def get_queryset(self):
        queryset = Post.objects.order_by("published").all()
        # This comes from the nested router
        # /api/authors/<author_pk>/posts/
        author_id = self.kwargs["author_pk"]
        queryset = queryset.filter(author=author_id)
        return queryset

    @action(detail=True, methods=["get"])
    def likes(self, request, **kwargs):
        post = self.get_object()
        queryset = Like.objects.order_by("-published").filter(post=post)
        data = LikeSerializer(queryset, many=True, context={"request": request}).data
        paginator = CustomPagination()
        return paginator.get_paginated_response(data, type="like")


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

    def perform_create(self, serializer):
        author_id = self.request.data["author"]
        post_id = self.kwargs["post_pk"]
        return serializer.save(author_id=author_id, post_id=post_id)

    @action(detail=True, methods=["get"])
    def likes(self, request, **kwargs):
        comment = self.get_object()
        queryset = Like.objects.order_by("-published").filter(comment=comment)
        data = LikeSerializer(queryset, many=True, context={"request": request}).data
        paginator = CustomPagination()
        return paginator.get_paginated_response(data, type="like")
