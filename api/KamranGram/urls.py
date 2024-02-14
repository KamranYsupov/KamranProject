from django.urls import path
from . import views

urlpatterns = [
    path('rooms/', views.RoomListAPIView.as_view()),
    path('room/<int:pk>/', views.DetailRoomAPIView.as_view(), name='room'),
    path('edit_room/<int:pk>/', views.EditRoomAPIView.as_view(), name='edit_room'),
    path('room/create/', views.CreateRoomAPIView.as_view(), name='create_room'),

    path('edit_message/<int:pk>/', views.EditMessageAPIView.as_view(), name='edit_message'),
]
