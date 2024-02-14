from rest_framework.permissions import SAFE_METHODS


def is_method_safe(request):
    if request.method in SAFE_METHODS:
        return True
