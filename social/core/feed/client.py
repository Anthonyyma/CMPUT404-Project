from requests import request
from json import load

def getExternPost(self, url: str) -> dict:
    """
    Get a post from an external server
    """

    response = request("GET", url)
    return load(response.json())