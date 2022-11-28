import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class ContentTypes(models.TextChoices):
    TEXT = "TXT", "text/plain"
    MD = "MD", "text/markdown"
    APP64 = "APP64", "application/base64"
    PNG = "PNG", "image/png"
    JPEG = "JPEG", "image/jpeg"


# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile_image = models.ImageField(default="defaultProPic.jpg", blank=True)
    github = models.URLField(blank=True, null=True)
    external_url = models.URLField(blank=True, null=True)


class Follow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )
    followee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers"
    )
    external_follower = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.follower} follows {self.followee}"


class FollowRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="outgoing_follow_requests"
    )
    followee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="incoming_follow_requests"
    )
    external_follower = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.follower} wants to follow {self.followee}"


CONTENT_TYPES = (
    ("TEXT", "text/plain"),
    ("MD", "text/markdown"),
    ("APP64", "application/base64"),
    ("PNG", "image/png"),
    ("JPEG", "image/jpeg"),
)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts", blank=True
    )
    title = models.TextField()
    source = models.TextField()
    origin = models.TextField()
    # use .get_content_type_display()
    content_type = models.CharField(max_length=5, choices=CONTENT_TYPES, default="TEXT")
    categories = models.TextField()  # just use space seperated strings for now lol
    content = models.TextField()
    # image = models.ImageField(blank=True, upload_to="media/")
    image = models.ImageField(blank=True)
    published = models.DateTimeField(auto_now_add=True)
    friends_only = models.BooleanField(default=False)
    unlisted = models.BooleanField(default=False)
    private_to = models.TextField(blank=True)

    def __str__(self):
        return f'"{self.title}" by {self.author}, posted at {self.published}'


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    external_author = models.URLField(blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    content_type = models.CharField(max_length=5, choices=ContentTypes.choices)
    published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} commented at {self.published}"


class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="likes", blank=True, null=True
    )
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="likes", blank=True, null=True
    )
    published = models.DateTimeField(auto_now_add=True)
    external_comment = models.URLField(
        blank=True, null=True
    )  # like is on an external comment
    external_post = models.URLField(blank=True, null=True)  # like is on external post
    external_user = models.URLField(blank=True, null=True)  # liker is an external user

    def __str__(self):
        return f"{self.user} liked {self.post} at {self.published}"


class Inbox(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="inbox")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    external_post = models.URLField(
        blank=True, null=True
    )  # external post has been sent to the inbox
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.external_post is not None:
            return f"{self.external_post} pushed to {self.user} at {self.timestamp}"
        return f"{self.post.title} pushed to {self.user}'s inbox"


class Node(models.Model):
    host = models.URLField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.host} - {self.username}"
