import json
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from articles.models import Article


class TestArticleGetRequest(APITestCase):

    """
    Test article get requests. Should return articles as a paginated response.

    """

    def setUp(self):
        self.user1 = User.objects.create_user(
            email='testuser1@example.com',
            password='testpassword',
            username='testusername1',
            is_staff='True',
        )

        self.user2 = User.objects.create_user(
            email='testuser1@example.com',
            password='testpassword',
            username='testusername2',
        )

        article1 = Article.objects.create(
            title='Visualizing SIMB3 data using Python',
            slug='simb3-python',
            status='Published',
        )
        article2 = Article.objects.create(
            title='Visualizing SIMB3 data using MATLAB',
            slug='coding-with-matlab',
            status='Published',
        )
        article3 = Article.objects.create(
            title='Cryosphere Innovation Style Guide',
            slug='style-guide',
            status='Published',
        )

        self.user1_access_token = str(AccessToken.for_user(self.user1))

    def test_public_get_article_thumbnails(self):
        url = reverse('articles-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

    def test_get_article_by_slug(self):
        url = reverse('articles-detail', args=['simb3-python'])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        self.assertEqual(response.data['slug'], 'simb3-python')
