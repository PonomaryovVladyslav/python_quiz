from rest_framework.permissions import BasePermission


class IsRegisterOrGetListOfUsers(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return request.method == 'POST' or bool(request.user and request.user.is_authenticated)

