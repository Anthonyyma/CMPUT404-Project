import re
from typing import Union
from core.models import Post, Comment, User
from django.conf import settings


def get_author_id_from_url(url: str) -> Union[str, None]:
    """
    Get the author id from the url
    """
    match = re.search(r"authors/(\w)+", url)
    return match.group(1) if match else None


def get_post_id_from_url(url: str) -> Union[str, None]:
    match = re.search(r"posts/(\w)+", url)
    return match.group(1) if match else None


def get_comment_id_from_url(url: str) -> Union[str, None]:
    """
    http://localhost/api/posts/1/comments/<comment_id> -> <comment_id>
    """
    match = re.search(r"comments/(\w)+", url)
    return match.group(1) if match else None


def get_author_url(author: User, request) -> str:
    """
    Returns the api url for an author
    """
    return f"{settings.API_HOST_PATH}authors/{author.id}/"


def get_post_url(post: Post, request) -> str:
    """
    Returns the api url for a post
    """
    return f"{settings.API_HOST_PATH}authors/{post.author.id}/posts/{post.id}/"


def get_comment_url(comment: Comment, request) -> str:
    """
    Returns the api url for a comment
    """
    return get_post_url(comment.post, request) + f"comments/{comment.id}/"
