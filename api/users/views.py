from django.contrib.auth import get_user_model
from rest_framework import viewsets

from Articles.permissions import IsAdminOrReadOnly
from api.pagination import ObjectsListAPIPagination
from api.permissions import IsUserOrReadOnly
from api.users.serializers import UserSerializer


class UserAPIViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    pagination_class = ObjectsListAPIPagination
    permission_classes = (IsUserOrReadOnly, )


