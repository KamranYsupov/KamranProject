from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.test import APITestCase, APIRequestFactory, APIClient

from api.comments.serializers import CommentListSerializer, CommentDetailSerializer
from api.service import all_items_match
from comments.models import Comment

factory = APIRequestFactory()
User = get_user_model()


class CommentsAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.data = {
            'comment': 'Комментарий'
        }

    def test_list_view(self):
        comment = Comment.objects.create(
            comment='Комментарий',
        )

        # Получаем значение поля HyperlinkedIdentityField
        request = factory.get(reverse('api:read_comment', kwargs={'pk': comment.id}))
        response = self.client.get(reverse('api:comments_list'))

        serializer_data = CommentListSerializer(comment, context={'request': Request(request)}).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(*response.data['results'], serializer_data)

    def test_read_detail_view(self):
        comment = Comment.objects.create(
            comment='Комментарий',
        )

        request = factory.get(reverse('api:read_comment', kwargs={'pk': comment.id}))
        response = self.client.get(reverse('api:read_comment', kwargs={'pk': comment.id}))

        serializer_data = CommentDetailSerializer(comment, context={'request': Request(request)}).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_invalid_create_view(self):
        """Проверка permission IsAuthenticated"""
        response = self.client.post(reverse('api:create_comment'), data=self.data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valid_create_view(self):
        user = User.objects.create_user(username='test_user', password='korkgprgcmv')
        token = Token.objects.create(user=user)

        self.client.force_authenticate(user=user, token=token)
        post_response = self.client.post(reverse('api:create_comment'), data=self.data)

        comment_obj = Comment.objects.get(comment=post_response.data.get('comment'))

        get_response = self.client.get(
            reverse(
                'api:read_comment',
                kwargs={'pk': comment_obj.id}
            ))

        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_response.data['author'], comment_obj.author.username)
        self.assertTrue(all_items_match(post_response.data, get_response.data))



