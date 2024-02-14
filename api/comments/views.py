from django.db.models import Q, Prefetch

from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from api.comments.serializers import CommentSerializer, CommentDetailSerializer, CreateCommentSerializer
from api.pagination import ObjectsListAPIPagination
from comments.models import Comment
from comments.service import deferred_comment_fields

comments = (
    Comment.objects
    .select_related('comment_author',
                    'parent__comment_author',
                    'parent__comment_post',
                    'comment_post',
                    'comment_video')
    .prefetch_related('likes', 'replies', 'replies__comment_author', 'replies__likes')
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
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(comment_author=self.request.user)


