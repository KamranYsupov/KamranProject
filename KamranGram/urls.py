from django.urls import path

from . import views

urlpatterns = [
   path('rooms/', views.Rooms.as_view(), name='rooms'),
   path('room/<int:room_id>/', views.DetailRoom.as_view(), name='room'),
   path('create/', views.CreateRoom.as_view(), name='create_room'),
   path('search/', views.RoomSearch.as_view(), name='room_search'),
   path('login_room/<int:room_id>/', views.login_room, name='login_room'),
]