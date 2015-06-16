from rest_framework import permissions


class IsOwnerOrShared(permissions.BasePermission):

    """
    Custom permission to only allow owners of an object to see it.
    """

    def has_object_permission(self, request, view, obj):
        # If we want to allow anon Read permissions to any request,
        # (GET, HEAD or OPTIONS safe requests only)
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        # TODO add sharing

        # permissions are only allowed to the owner of the snippet.

        if hasattr(obj, "shared_with_public"):
            if obj.shared_with_public:
                return True
        if hasattr(obj, "site"):
            if obj.site.shared_with_public:
                return True


        return obj.user == request.user
