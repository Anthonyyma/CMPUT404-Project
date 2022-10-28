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
    display_name = models.CharField(max_length=255, blank=True, null=True)
    profile_image = models.ImageField(upload_to="profile_images", blank=True)
    github = models.URLField(blank=True)


class Follow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )
    followee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers"
    )

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

    def __str__(self):
        return f"{self.follower} wants to follow {self.followee}"


CONTENT_TYPES = (
    ("TEXT", "text/plain"),
    ("MD", "text/markdown"),
    ("APP64", "application/base64"),
    ("PNG", "image/png"),
    ("JPEG", "image/jpeg")
)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
     related_name="posts", blank=True)
    title = models.TextField()
    source = models.TextField()
    origin = models.TextField()
    # use .get_content_type_display()
    content_type = models.CharField(
        max_length=5, choices=CONTENT_TYPES, default="TEXT"
    )
    categories = models.TextField()  # just use space seperated strings for now lol
    content = models.TextField()
    image = models.ImageField(blank=True, upload_to="media/")
    published = models.DateTimeField(auto_now_add=True)
    friends_only = models.BooleanField(default=False)
    unlisted = models.BooleanField(default=False)

    def __str__(self):
        return f'"{self.title}" by {self.author}, posted at {self.published}'


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
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

    def __str__(self):
        return f"{self.user} liked {self.post} at {self.published}"


class Inbox(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="inbox")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post.title} pushed to {self.user}'s inbox"
