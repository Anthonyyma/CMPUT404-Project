import re
from typing import Union

from core.models import Comment, Post, User
from django.conf import settings


def get_author_id_from_url(url: str) -> Union[str, None]:
    """
    Get the author id from the url
    """
    match = re.search(r"authors/([\w\-]+)", url)
    return match.group(1) if match else None


def get_post_id_from_url(url: str) -> Union[str, None]:
    match = re.search(r"posts/([\w\-]+)", url)
    return match.group(1) if match else None


def get_comment_id_from_url(url: str) -> Union[str, None]:
    """
    http://localhost/api/posts/1/comments/<comment_id> -> <comment_id>
    """
    match = re.search(r"comments/(\w)+", url)
    return match.group(1) if match else None


def get_author_url(author: User) -> str:
    """
    Returns the api url for an author
    """
    if author.external_url is not None:
        return author.external_url
    return f"{settings.API_HOST_PATH}authors/{author.id}/"


def get_post_url(post: Post) -> str:
    """
    Returns the api url for a post
    """
    return f"{settings.API_HOST_PATH}authors/{post.author.id}/posts/{post.id}/"


def get_comment_url(comment: Comment) -> str:
    """
    Returns the api url for a comment
    """
    return get_post_url(comment.post) + f"comments/{comment.id}/"


def get_external_user_inbox_url(user: User) -> str:
    """
    Returns the api url for a user's inbox
    """
    suffix = "inbox/" if user.external_url.endswith("/") else "/inbox/"
    return user.external_url + suffix
