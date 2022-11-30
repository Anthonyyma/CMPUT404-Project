from core.models import FollowRequest, User, Post
from core.path_utils import get_author_url, get_post_url
from rest_framework import status
from rest_framework.test import APITestCase


class InboxText(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="test1")
        self.post1 = Post.objects.create(
            author=self.user1, content="post1", friends_only=False
        )

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

    def test_external_post(self):
        data = {
            "type": "post",
            "title": "A post title about a post about web dev",
            "id": "http://127.0.0.1:5454/authors/9de17f20658e/posts/764bd9e",
            "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
            "origin": "http://whereitcamefrom.com/posts/zzzzz",
            "description": "This post discusses stuff -- brief",
            "contentType": "text/plain",
            "content": "Þā wæs on burgum Bēowulf Scyldinga, lēof lēod-cyning",
            "author": {
                "type": "author",
                "id": "http://127.0.0.1:5454/authors/9de17f20658e/",
                "host": "http://127.0.0.1:5454/",
                "displayName": "Lara Croft",
                "url": "http://127.0.0.1:5454/authors/9de17f20658e/",
                "github": "http://github.com/laracroft",
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
            },
            "categories": ["web", "tutorial"],
        }
        inbox_path = f"/api/authors/{self.user1.id}/inbox/"
        resp = self.client.post(inbox_path, data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.user1.inbox.count(), 1)
        inbox = self.user1.inbox.filter(external_post=data["id"]).first()
        self.assertIsNotNone(inbox)

    def test_external_like_on_local_post(self):
        post_url = get_post_url(self.post1)
        data = {
            "type": "Like",
            "author": {
                "type": "author",
                "id": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                "host": "http://127.0.0.1:5454/",
                "displayName": "Lara Croft",
                "url": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                "github": "http://github.com/laracroft",
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
            },
            "object": post_url,
        }
        inbox_path = f"/api/authors/{self.user1.id}/inbox/"
        resp = self.client.post(inbox_path, data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
