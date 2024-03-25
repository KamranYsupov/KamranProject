from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from api.articles.serializers import (
    ArticlesListSerializer,
    ReadArticleSerializer,
    ArticleCreateSerializer,
    ArticleEditSerializer,
)
from articles.models import Article


class ArticlesSerializerTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.article = Article.objects.create(
            title='Статья',
            slug='slug',
            is_published=1,
            author=None,
        )

    def test_list_serializer(self):
        request = self.factory.get(reverse('api:articles_list'))

        expected_data = {
            'id': 1,
            'title': 'Статья',
            'content': '',
            'slug': 'slug',
            'photo': None,
            'time_create': '24-03-2024 09:15:51',
            'is_published': 1,
            'author': 'None',
            'views': 1,
            'likes': 0,
            'like_percent': 0,
            'comments_count': 0,
            'read_url': 'http://testserver/api/v1/kamran-project/articles/read/slug/'
        }
        serializer_data = ArticlesListSerializer(self.article, context={'request': Request(request)}).data

        # Время создания всегда будет разным, поэтому удаляем
        expected_data.pop('time_create')
        serializer_data.pop('time_create')

        self.assertEqual(serializer_data, expected_data)

    def test_read_serializer(self):
        request = self.factory.get(
            reverse('api:read_article', kwargs={'post_slug': self.article.slug})
        )
        expected_data = {
            'id': 1,
            'title': 'Статья',
            'content': '',
            'slug': 'slug',
            'photo': None,
            'time_create': '24-03-2024 09:15:51',
            'is_published': 1,
            'author': 'None',
            'views': 1,
            'likes': 0,
            'like_percent': 0,
            'post_comments': [],
            'comments_count': 0,
        }

        serializer_data = ReadArticleSerializer(self.article, context={'request': Request(request)}).data

        expected_data.pop('time_create')
        serializer_data.pop('time_create')

        self.assertEqual(serializer_data, expected_data)

    def test_create_serializer(self):
        expected_data = {
            'title': 'Статья',
            'slug': 'slug',
            'content': '',
            'photo': None,
            'is_published': 1,
            'link': 'http://testserver' + reverse(
                'api:read_article', kwargs={'post_slug': self.article.slug}
            )
        }

        request = self.factory.get(
            reverse('api:read_article', kwargs={'post_slug': self.article.slug})
        )

        serializer_data = ArticleCreateSerializer(
            self.article, context={'request': Request(request)}).data

        self.assertEqual(serializer_data, expected_data)

    def test_edit_serializer(self):
        expected_data = {
            'title': 'Статья',
            'slug': 'slug',
            'content': '',
            'photo': None,
            'is_published': 1
        }

        serializer_data = ArticleEditSerializer(self.article).data

        self.assertEqual(serializer_data, expected_data)
