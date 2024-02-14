from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.comments import views

urlpatterns = [
    path('', views.CommentsListAPIView.as_view()),
    path('create/', views.CreateCommentAPIView.as_view(), name='create_comment'),
    path('<int:pk>/', views.CommentDetailAPIView.as_view(), name='read_comment'),
]
