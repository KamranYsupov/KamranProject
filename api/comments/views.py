from django.db.models import Q, Prefetch, Count

from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from api.comments.serializers import CommentSerializer, CommentDetailSerializer, CreateCommentSerializer
from api.pagination import ObjectsListAPIPagination
from comments.models import Comment
from comments.service import deferred_comment_fields

selected_fields = ['author', 'parent', 'user_to_reply', 'post', 'video']

comments = (
    Comment.objects
    .defer(*deferred_comment_fields)
    .select_related(*selected_fields)
    .prefetch_related('likes',
                      Prefetch('replies',
                               queryset=Comment.objects
                               .select_related(*selected_fields)
                               .prefetch_related('likes')))
    .annotate(likes_count=Count('likes'))
    .order_by('-likes_count', '-time_create')
)


class CommentDetailAPIView(generics.RetrieveAPIView):
    queryset = comments
    serializer_class = CommentDetailSerializer


class CommentsListAPIView(generics.ListAPIView):
    queryset = comments
    serializer_class = CommentSerializer
    pagination_class = ObjectsListAPIPagination


class CreateCommentAPIView(generics.CreateAPIView):
    queryset = comments
    serializer_class = CreateCommentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
