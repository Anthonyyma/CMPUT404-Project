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


def get_external_user_inbox_url(user: Union[User, str]) -> str:
    """
    Returns the api url for a user's inbox
    """
    base_url = user if isinstance(user, str) else user.external_url
    # this is a hack, team9 author ids point to the frontend instead of the api
    # https://team9.herokuapp.com/authors/abc/inbox/ ->
    # https://team9.herokuapp.com/service/authors/abc/inbox/
    base_url = format_team9_author_url(base_url)
    suffix = "inbox/" if base_url.endswith("/") else "/inbox/"
    if "team9" in base_url:
        suffix = suffix[:-1]  # no trailing slash for team9
    return base_url + suffix


def format_team9_author_url(url: str) -> str:
    """
    https://team9.herokuapp.com/authors/abc/ ->
    https://team9.herokuapp.com/service/authors/abc/
    """
    if "team9" in url and "service" not in url:
        parts = re.split(r"herokuapp\.com", url)
        parts.insert(1, "herokuapp.com/service")
        return "".join(parts)
    return url
