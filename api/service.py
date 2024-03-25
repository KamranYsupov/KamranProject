from rest_framework.permissions import SAFE_METHODS


def is_method_safe(request):
    if request.method in SAFE_METHODS:
        return True


def all_items_match(member: dict, container: dict):
    return all(item in container.items() for item in member.items())
