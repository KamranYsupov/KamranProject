import json

from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.test import APITestCase, APIRequestFactory, APIClient

from django.conf import settings
from api.articles.serializers import ArticlesListSerializer, ReadArticleSerializer, ArticleEditSerializer
from articles.models import Article

factory = APIRequestFactory()
User = get_user_model()


class ArticlesAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_view(self):
        article = Article.objects.create(
            title='Статья',
            slug='slug',
            is_published=1,
            author=None,
        )
        request = factory.get(reverse('api:read_article', kwargs={'post_slug': article.slug}))
        response = self.client.get(reverse('api:articles_list'))

        serializer_data = ArticlesListSerializer(article, context={'request': Request(request)}).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(*response.data['results'], serializer_data)

    def test_invalid_create_view(self):
        """Проверка permission IsAuthenticated"""
        data = {
            'title': 'Статья',
            'slug': 'slug',
            'is_published': 1,
        }
        response = self.client.post(reverse('api:create_article'), data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valid_create_view(self):
        user = User.objects.create_user(username='test_user', password='sfkdssdvjf12435')
        user.save()

        token = Token.objects.create(user=user)

        data = {
            'title': 'Статья',
            'slug': 'slug',
            'is_published': 1,  # не писать True
        }
        self.client.force_authenticate(user=user, token=token)
        response = self.client.post(reverse('api:create_article'), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_detail_view(self):
        article = Article.objects.create(
            title='Статья',
            slug='slug',
            is_published=1,
            author=None,
        )

        response = self.client.get(reverse('api:read_article', kwargs={'post_slug': article.slug}))

        serializer_data = ReadArticleSerializer(article).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_not_auth_update_view(self):
        """Проверка permission IsAuthenticated"""
        article = Article.objects.create(
            title='Статья',
            slug='slug',
            is_published=1,
            author=None,
        )

        data = {
            'is_published': 0
        }

        response = self.client.patch(
            reverse('api:edit_article', kwargs={'post_slug': article.slug}),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permission_update_view(self):
        """Проверка permission IsOwnerOrReadOnly"""
        user_1 = User.objects.create_user(username='test_user1', password='sfkdssdvjf12435_1')
        user_1.save()
        article = Article.objects.create(
            title='Статья',
            slug='slug',
            is_published=1,
            author=user_1,
        )

        user_2 = User.objects.create_user(username='test_user2', password='sfkdssdvjf12435_2')
        user_2.save()
        token_2 = Token.objects.create(user=user_2)

        self.client.force_authenticate(user=user_2, token=token_2)

        data = {
            'is_published': 0
        }

        response = self.client.patch(
            reverse('api:edit_article', kwargs={'post_slug': article.slug}),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valid_patch_update_view(self):
        """Проверка HTTP метода PATCH"""
        user = User.objects.create_user(username='test_user', password='sfkdssdvjf12435')
        user.save()

        article = Article.objects.create(
            title='Статья',
            slug='slug',
            is_published=1,
            author=user,
        )

        token = Token.objects.create(user=user)

        self.client.force_authenticate(user=user, token=token)

        old_serializer_data = ArticleEditSerializer(article).data

        data = {'is_published': 0, }
        response = self.client.patch(
            reverse('api:edit_article', kwargs={'post_slug': article.slug}),
            data=data
        )

        updated_article = Article.objects.get(id=1)

        updated_serializer_data = ArticleEditSerializer(updated_article).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, old_serializer_data)
        self.assertEqual(response.data, updated_serializer_data)

    def test_valid_put_update_view(self):
        """Проверка HTTP метода PUT"""
        user = User.objects.create_user(username='test_user', password='sfkdssdvjf12435')
        user.save()

        article = Article.objects.create(
            title='Статья',
            slug='slug',
            is_published=1,
            author=user,
        )

        token = Token.objects.create(user=user)

        self.client.force_authenticate(user=user, token=token)

        data = {
            'title': 'Измененная статья',
            'slug': 'updated_slug',
            'is_published': 0,
        }
        old_serializer_data = ArticleEditSerializer(article).data

        response = self.client.put(
            reverse('api:edit_article', kwargs={'post_slug': article.slug}),
            data=data
        )

        updated_article = Article.objects.get(id=1)

        updated_serializer_data = ArticleEditSerializer(updated_article).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, old_serializer_data)
        self.assertEqual(response.data, updated_serializer_data)

    def test_delete_view(self):
        pass
