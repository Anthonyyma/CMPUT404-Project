from core.models import Comment, Post, User
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
        self.assertEqual(post["author"]["displayName"], self.user1.username)

    def test_get_posts_returns_comments_correctly(self):
        # create one comment on each post
        Comment.objects.create(post=self.post1, author=self.user2, content="c1")
        Comment.objects.create(post=self.post2, author=self.user2, content="c1")
        path = f"/api/authors/{self.user1.id}/posts/{self.post1.id}/"
        resp = self.client.get(path, follow=True)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual(data["count"], 1)
        # url to comments is correct
        self.assertTrue(
            f"authors/{self.post1.author.id}/posts/{self.post1.id}/comments"
            in data["comments"]
        )
        # user2 made the only comment on this post
        self.assertEqual(
            data["commentsSrc"]["comments"][0]["author"]["displayName"],
            self.user2.username,
        )

    def test_delete_post(self):
        path = f"/api/authors/{self.user1.id}/posts/{self.post1.id}/"
        resp = self.client.delete(path)

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post1.id).exists())

    def test_create_post(self):
        path = f"/api/authors/{self.user1.id}/posts/"
        resp = self.client.post(
            path,
            {
                "author": self.user1.id,
                "content": "new post",
                "visibility": "PUBLIC",
                "contentType": "text/plain",
                "source": "http://www.example.com",
                "origin": "http://www.example.com",
            },
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Post.objects.filter(content="new post", author=self.user1).exists()
        )

    def test_create_comment(self):
        path = f"/api/authors/{self.user1.id}/posts/{self.post1.id}/comments/"
        resp = self.client.post(
            path,
            {
                "author": self.user2.id,
                "comment": "new comment",
                "contentType": "text/markdown",
            },
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Comment.objects.filter(
                author=self.user2, post=self.post1, content="new comment"
            ).exists()
        )
