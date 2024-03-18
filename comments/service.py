from django.db.models import Prefetch

from .models import Comment

deferred_comment_fields = [
    'author__password', 'author__last_login',
    'author__is_superuser', 'author__first_name', 'author__last_name',
    'author__email', 'author__is_staff', 'author__is_active',
    'author__date_joined', 'author__date_birth',
    'author__is_subscribed_on_quotes',
    'author__is_subscribed_on_weather', 'author__id', 'video__id',
]

post_comments_prefetch = Prefetch('post_comments',
                                  queryset=Comment.objects.select_related('author', )
                                  .prefetch_related('likes', 'replies'))

video_comments_prefetch = Prefetch('video_comments',
                                   queryset=Comment.objects.select_related('author', )
                                   .prefetch_related('likes', 'replies'))

prefetched_replies = Prefetch('replies',
                              queryset=Comment.objects.select_related(
                                  'author',
                              )
                              .prefetch_related(
                                  'likes',
                                  'replies_to_replies__author',
                                  'replies_to_replies__likes'
                              ))
