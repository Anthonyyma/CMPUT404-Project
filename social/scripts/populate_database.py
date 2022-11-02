# this can be pasted into the django shell to populate the database with some test data
from core.models import ContentTypes, Follow, FollowRequest, Post, User

User.objects.all().delete()
User.objects.create(username="test1", password="test1")
Post.objects.create(
    author=User.objects.get(username="test1"),
    content="This is a test post",
    content_type=ContentTypes.TEXT,
    categories="test,funny",
)
