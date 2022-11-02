from core.models import Post, User
from rest_framework import status
from rest_framework.test import APITestCase


class AuthorTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="test1")
        self.user2 = User.objects.create(username="test2")
        self.post1 = Post.objects.create(
            author=self.user1, content="post1", friends_only=False
        )
        self.post2 = Post.objects.create(
            author=self.user2, content="post2", friends_only=False
        )

    def test_get_posts(self):
        path = f"/api/authors/{self.user1.id}/posts/"
        resp = self.client.get(path, follow=True)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.json()
        self.assertEqual(data["type"], "post")
        self.assertEqual(len(data["items"]), 1)
        post = data["items"][0]
        self.assertEqual(post["content"], self.post1.content)
        self.assertEqual(post["visibility"], "PUBLIC")
        # self.assertEqual(post["author"]["displayName"], self.user1.username)
