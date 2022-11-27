from core.models import FollowRequest, User
from core.path_utils import get_author_url
from rest_framework import status
from rest_framework.test import APITestCase


class InboxText(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="test1")

    def test_external_follow_request(self):
        path = f"/api/authors/{self.user1.id}/inbox/"
        external_host = "http://othersite.com"
        external_user_url = external_host + "/authors/1d698d25ff008f7538453c120f581471"
        resp = self.client.post(
            path,
            {
                "type": "Follow",
                "actor": {
                    "type": "author",
                    "id": external_user_url,
                    "host": external_host,
                    "displayName": "Greg Johnson",
                    "github": "http://github.com/gjohnson",
                    "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
                },
                "object": {
                    "type": "author",
                    "id": get_author_url(self.user1),
                },
            },
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            FollowRequest.objects.filter(
                followee=self.user1, follower__external_url=external_user_url
            ).exists()
        )
