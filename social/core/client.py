import random
import re
from typing import Dict

import requests
from core.authors.serializers import AuthorSerializer
from core.models import User
from core.path_utils import (
    format_team9_author_url,
    get_author_url,
    get_external_user_inbox_url,
)
from rest_framework import status
from rest_framework.response import Response


def get_creds(url: str):
    if "cmsjmnet" in url:
        return ("team8", "team8")
    if "team9" in url:
        return ("admin", "admin")
    if "socialdistribution-cmput404" in url:
        return ("Novadrive", "B8fmmUSwpxYcmsm")
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
    resp = requests.get(post_url, auth=get_creds(post_url))
    return resp.json()


def fetch_external_user(user_url: str):
    resp = requests.get(user_url, auth=get_creds(user_url))
    return resp.json()


def fetch_posts_from_external_author(user: User):
    if user.external_url is None:
        return []
    path = (
        user.external_url + "posts/"
        if user.external_url.endswith("/")
        else user.external_url + "/posts/"
    )
    if "team9" in path:
        path = format_team9_author_url(path)
    #     path = path[:-1]  # no trailing slashes in team9
    print("fetching posts from", path)
    resp = requests.get(path, auth=get_creds(path))
    if not resp.ok:
        print(f"Error getting posts from {path}")
        print(resp.text)
        return []
    data = resp.json()
    if "items" in data:
        return data["items"]
    if "results" in data:
        return data["results"]
    elif isinstance(data, list):
        return data
    print("Couldn't find posts in response", path, data)
    return []


def send_external_follow_request(local_user: User, external_user_url: str, request):
    data = {
        "type": "follow",
        "actor": AuthorSerializer(local_user, context={"request": request}).data,
        "object": {
            "id": external_user_url,
        },
    }
    if "cmsjmnet" in external_user_url:
        data = {"items": [data], "author": get_author_url(local_user)}
    url = get_external_user_inbox_url(external_user_url)
    resp = requests.post(url, json=data, auth=get_creds(external_user_url))
    print(data)
    print(resp, resp.json())
    return resp


def send_post_to_external_user(post_data: Dict, external_user: User):
    post_data["description"] = post_data.get("content", " ")
    url = get_external_user_inbox_url(external_user)
    msg = post_data
    if "cmsjmnet" in url:
        msg = {
            "items": [post_data],
            "author": post_data["author"],
        }
    requests.post(url, json=msg, auth=get_creds(url))


def sync_external_authors():
    team11_url = "https://cmsjmnet.herokuapp.com/authors/"
    team9_url = "https://team9-socialdistribution.herokuapp.com/service/authors/"
    team6_url = "https://socialdistribution-cmput404.herokuapp.com/authors/"

    team11_authors = requests.get(team11_url, auth=get_creds(team11_url)).json()
    # no need for auth for team9
    team9_authors = requests.get(team9_url, auth=get_creds(team9_url)).json()
    team6_authors = requests.get(team6_url, auth=get_creds(team6_url)).json()

    all_authors = []

    try:
        all_authors.extend(team11_authors["results"])
    except:
        pass
    try:
        all_authors.extend(team9_authors["items"])
    except:
        pass
    try:
        all_authors.extend(team6_authors["items"])
    except:
        pass

    for author in all_authors:
        create_update_external_authors(author)


def create_update_external_authors(author):
    """Take argument of the author in json format
    and add it to the database.

    If duplicate usernames are found then generate
    a random 6 digit number and append it to the end"""
    from_database_url = User.objects.filter(external_url=author["url"]).first()
    from_database_username = User.objects.filter(username=author["displayName"]).first()

    if from_database_username is not None:
        # https://stackoverflow.com/questions/59318332/generate-random-6-digit-id-in-python
        random_id = " ".join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])

        author["displayName"] = author["displayName"] + random_id

    if from_database_url is not None:
        pass
    else:
        serializer = AuthorSerializer(data=author)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return serializer.save(external_url=author["id"])


def get_comments(comments_url: str):
    resp = requests.get(comments_url)
    if resp.ok:
        return resp.json()["items"]
    print(f"Error getting comments from {comments_url}")
    print(resp)
    return []
