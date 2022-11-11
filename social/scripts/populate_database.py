# this can be pasted into the django shell to populate the database with some test data
from core.models import Comment, ContentTypes, Follow, Post, User

User.objects.all().delete()
user1 = User.objects.create(username="user1", password="pass1")
user2 = User.objects.create(username="user2", password="pass2")

Follow.objects.create(followee=user1, follower=user2)  # user2 follows user1

post1 = Post.objects.create(
    author=user1,
    content="This is a test post",
    content_type=ContentTypes.TEXT,
    categories="test,funny",
)

# some test comments on post1
Comment.objects.create(post=post1, author=user1, content="comment1")
Comment.objects.create(post=post1, author=user2, content="comment2")

post2 = Post.objects.create(
    author=user2,
    content="This is a second test post",
    content_type=ContentTypes.TEXT,
    categories="test,serious",
)

# some test comments on post2
Comment.objects.create(post=post2, author=user2, content="comment1")
Comment.objects.create(post=post2, author=user2, content="comment2")
