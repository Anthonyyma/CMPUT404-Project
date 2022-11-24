import re
from typing import Union


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
