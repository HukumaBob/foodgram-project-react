from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):
    """
    Allows access only to authenticated users with admin role.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and has admin role
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        # Same permission requirements as for the list view
        return self.has_permission(request, view)


class IsAdminOrStuffPermission(permissions.BasePermission):
    """
    Allows access to staff members or authenticated users with admin role.
    """

    def has_permission(self, request, view):
        # Check if the user is staff or authenticated with admin role
        return (
            request.user.is_staff
            or (
                request.user.is_authenticated
                and request.user.is_admin
            )
        )


class IsAuthorOrModeratorPermission(permissions.BasePermission):
    """
    Allows access to authors, moderators, or users with admin role.
    """

    def has_object_permission(self, request, view, obj):
        # Allow safe methods (GET, HEAD, OPTIONS) to anyone
        # Allow access to the author, moderators, or users with admin role
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )


class IsAuthorOrModerator(permissions.BasePermission):
    """
    Allows access to authors, moderators, or authenticated users.
    """

    def has_permission(self, request, view):
        # Allow safe methods (GET, HEAD, OPTIONS) to anyone
        # Allow access to authenticated users
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        # Allow safe methods (GET, HEAD, OPTIONS) to anyone
        # Allow access to the author, moderators, or users with admin role
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allows access to authenticated users with admin role,
    and read-only access to anyone.
    """

    def has_permission(self, request, view):
        # Allow safe methods (GET, HEAD, OPTIONS) to anyone
        # Allow access to authenticated users with admin role
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.is_admin
            )
        )


class ReadOnly(permissions.BasePermission):
    """
    Allows read-only access to anyone.
    """

    def has_permission(self, request, view):
        # Allow safe methods (GET, HEAD, OPTIONS) to anyone
        return request.method in permissions.SAFE_METHODS
