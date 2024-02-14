from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.users import views
users_router = SimpleRouter()
users_router.register(r'users', views.UserAPIViewSet)

urlpatterns = [

]

urlpatterns += users_router.urls
