import re

import requests
from core.authors.serializers import AuthorSerializer
from core.models import User


def get_creds(url: str):
    if "cmsjmnet" in url:
        return ("team8", "team8")
    return None


def fetch_github_feed(user: User):
    if user.github is None:
        return None
    pattern = r"github\.com\/([^\/]+)"
    handle = re.match(pattern, user.github).group(1)
    url = "https://api.github.com/users/" + handle + "/events"
    resp = requests.get(url)
    return resp.json()


def fetch_external_post(post_url: str):
    creds = None
    if "cmsjmnet" in post_url:
        creds = ("team8", "team8")
    resp = requests.get(post_url, auth=creds)
    return resp.json()


def send_external_follow_request(local_user: User, external_user_url: str, request):
    data = {
        "type": "follow",
        "actor": AuthorSerializer(local_user, context={"request": request}).data,
        "object": {
            "id": external_user_url,
        },
    }
    requests.post(
        external_user_url + "/inbox", json=data, auth=get_creds(external_user_url)
    )
