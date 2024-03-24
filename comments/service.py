from django.db.models import Prefetch

from .models import Comment

deferred_comment_fields = [
    'author__password', 'author__last_login',
    'author__is_superuser', 'author__first_name', 'author__last_name',
    'author__email', 'author__is_staff', 'author__is_active',
    'author__date_joined', 'author__date_birth',
    'author__is_subscribed_on_quotes',
    'author__is_subscribed_on_weather',
    'user_to_reply__password', 'user_to_reply__last_login',
    'user_to_reply__is_superuser', 'user_to_reply__first_name', 'user_to_reply__last_name',
    'user_to_reply__email', 'user_to_reply__is_staff', 'user_to_reply__is_active',
    'user_to_reply__date_joined', 'user_to_reply__date_birth',
    'user_to_reply__is_subscribed_on_quotes',
    'user_to_reply__is_subscribed_on_weather',
    'author__id', 'video__id',

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
