from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from api.articles.serializers import ArticlesListSerializer
from articles.models import Article

factory = APIRequestFactory()


class ArticlesSerializerTestCase(TestCase):
    def test_list_serializer(self):
        article = Article.objects.create(
            title='Статья',
            slug='slug',
            is_published=True,
            author=None,
        )
        request = factory.get(F'{settings.PROJECT_URL}/api/v1/kamran-project/articles/read/{article.slug}/')

        expected_data = {
            'id': 1,
            'title': 'Статья',
            'content': '',
            'slug': 'slug',
            'photo': None,
            'time_create': '24-03-2024 09:15:51',
            'is_published': True,
            'author': 'None',
            'views': 1,
            'likes': 0,
            'like_percent': 0,
            'comments_count': 0,
            'read_url': 'http://testserver/api/v1/kamran-project/articles/read/slug/'
        }
        serializer_data = ArticlesListSerializer(article, context={'request': Request(request)}).data

        expected_data.pop('time_create')
        serializer_data.pop('time_create')

        self.assertEqual(serializer_data, expected_data)

