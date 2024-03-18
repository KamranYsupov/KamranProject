from django.urls import path
from . import views

urlpatterns = [
    path('<int:object_id>/like_comment/<int:comment_id>/<int:user_to_reply_id>',
         views.like_comment, name='like_comment'),
    path('<int:object_id>/reply_comment/<int:parent_id>/<int:user_to_reply_id>',
         views.reply_comment, name='reply_comment'),
    path('<int:object_id>/reply_to_reply/<int:parent_id>/<int:user_to_reply_id>',
         views.reply_to_reply, name='reply_to_reply'),
]