from django.test import TestCase
from django.urls import reverse
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from api.comments.serializers import (
    CommentListSerializer,
    CommentDetailSerializer,
    CreateCommentSerializer
)

from comments.models import Comment


class CommentsSerializerTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.comment = Comment.objects.create(
            comment='Комментарий'
        )

    def test_list_serializer(self):
        expected_data = {
            'id': 1,
            'author': None,
            'comment': 'Комментарий',
            'likes': 0,
            'time_create': '2024-03-24T11:35:09.949954+03:00',
            'video': None,
            'post': None,
            'parent': None,
            'replies_count': 0,
            'link': 'http://testserver' + reverse(
                'api:read_comment', kwargs={'pk': self.comment.id}
            )
        }

        request = self.factory.get(reverse('api:read_comment', kwargs={'pk': self.comment.id}))

        serializer_data = CommentListSerializer(self.comment, context={'request': Request(request)}).data

        # Время создания всегда будет разным, поэтому удаляем
        expected_data.pop('time_create')
        serializer_data.pop('time_create')

        self.assertEqual(serializer_data, expected_data)

    def test_detail_serializer(self):
        expected_data = {
            'id': 1,
            'author': None,
            'comment': 'Комментарий',
            'likes': 0,
            'time_create': '2024-03-25T14:14:12.406504+03:00',
            'video': None,
            'post': None,
            'parent': None,
            'replies': [],
            'user_to_reply': None,
            'is_reply_to_reply': 0
        }

        serializer_data = CommentDetailSerializer(self.comment).data

        # Время создания всегда будет разным, поэтому удаляем
        expected_data.pop('time_create')
        serializer_data.pop('time_create')

        self.assertEqual(serializer_data, expected_data)

    def test_create_serializer(self):
        serializer_data = CreateCommentSerializer(self.comment).data

        expected_data = {
            'comment': 'Комментарий',
            'post': None,
            'video': None,
            'parent': None,
            'user_to_reply': None,
            'is_reply_to_reply': 0
        }

        self.assertEqual(serializer_data, expected_data)
