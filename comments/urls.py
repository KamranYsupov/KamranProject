from django.urls import path
from . import views

urlpatterns = [
    path('<int:object_id>/like_comment/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('<int:object_id>/reply_comment/<int:parent_id>/', views.reply_comment, name='reply_comment')
]