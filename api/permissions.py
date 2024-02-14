from rest_framework.permissions import BasePermission, SAFE_METHODS
from .service import is_method_safe


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_method_safe(request)
        return obj.author == request.user or bool(request.user and request.user.is_staff)


class IsRoomCreatorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_method_safe(request)
        return obj.creator == request.user or bool(request.user and request.user.is_staff)


class IsSenderOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_method_safe(request)
        return obj.sender == request.user or bool(request.user and request.user.is_staff)


class IsUserOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_method_safe(request)
        return obj == request.user or bool(request.user and request.user.is_staff)
