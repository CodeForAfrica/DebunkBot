from rest_framework import permissions


class IsGetRequest(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        else:
            return request.user and request.user.is_authenticated
