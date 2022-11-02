from core.models import Post
from core.pagination import labelled_pagination
from core.posts.serializers import PostSerializer
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
