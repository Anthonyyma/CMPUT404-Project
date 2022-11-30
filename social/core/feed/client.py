from json import load

from requests import request


def getExternPost(self, url: str) -> dict:
    """
    Get a post from an external server
    """

    response = request("GET", url)
    return load(response.json())