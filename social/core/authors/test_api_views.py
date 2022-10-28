import json

from core.models import Follow, User
from rest_framework import status
from rest_framework.test import APITestCase


class AuthorTest(APITestCase):
    def setUp(self):
        self.user1 = User(
            username="test1", password="test1", github="http://github.com/test1"
        )
        self.user1.save()
        self.user2 = User(username="test2", password="test1")
        self.user2.save()
        # user2 follows user1
        Follow.objects.create(follower=self.user2, followee=self.user1).save()

    def login(self, user):
        self.client.force_authenticate(user=user)

    def test_get_authors_paginated(self):
        resp = self.client.get("/api/authors", follow=True)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.json()
        self.assertEqual(data["type"], "authors")
        self.assertIn("items", data)
        self.assertEqual(len(data["items"]), 2)

    def test_get_author(self):
        path = f"/api/authors/{self.user1.id}/"
        resp = self.client.get(path, follow=True)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset(
            {
                "type": "author",
                "displayName": self.user1.username,
                "github": self.user1.github,
            },
            resp.json(),
        )

    def test_update_author(self):
        path = f"/api/authors/{self.user1.id}/"
        new_github = "http://github.com/new-github"
        self.login(self.user1)
        resp = self.client.post(
            path,
            json.dumps({"github": new_github}),
            content_type="application/json",
        )

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.github, new_github)

    def test_cannot_update_other_authors(self):
        path = f"/api/authors/{self.user1.id}/"
        new_github = "http://github.com/new-github"
        self.login(self.user2)
        resp = self.client.post(
            path,
            json.dumps({"github": new_github}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_author_followers(self):
        path = f"/api/authors/{self.user1.id}/followers/"
        resp = self.client.get(path, follow=True)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual(len(data["items"]), 1)
        self.assertEqual(data["type"], "followers")
        follower = data["items"][0]
        self.assertEqual(follower["displayName"], self.user2.username)

    def test_get_author_followers_does_not_return_followees(self):
        # user2 follows user1, so user1 should not be returned
        path = f"/api/authors/{self.user2.id}/followers/"
        resp = self.client.get(path, follow=True)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual(len(data["items"]), 0)
