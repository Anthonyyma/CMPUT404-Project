import re

import requests
from core.models import User


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
