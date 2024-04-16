from django.contrib import admin
from user.models import NilvaUser


class NilvaUserAdmin(admin.ModelAdmin):
    """
    Customizes the administration interface for the NilvaUser model.

    Methods:
        - get_queryset(self, request): Filters the queryset based on user permissions.
        - has_change_permission(self, request, obj=None): Checks if the user has permission to change a user object.
        - has_delete_permission(self, request, obj=None): Checks if the user has permission to delete a user object.
    """

    list_display = ("email", "username")

    def get_queryset(self, request):
        """
        Filters the queryset based on user permissions.

        Args:
            request: The HTTP request object.

        Returns:
            Queryset: Filtered queryset based on user permissions.
        """
        qs = super().get_queryset(request)
        if request.user.permissions == NilvaUser.ADMIN:
            return qs  # Allow admin users to see all users
        return qs.filter(id=request.user.id)  # Only show the user's own profile

    def has_change_permission(self, request, obj=None):
        """
        Checks if the user has permission to change a user object.

        Args:
            request: The HTTP request object.
            obj (NilvaUser): The user object being modified.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        if obj is not None and request.user.permissions == NilvaUser.ADMIN:
            return True  # Admin users can change any user object
        return obj == request.user  # Normal users can only change their own profile

    def has_delete_permission(self, request, obj=None):
        """
        Checks if the user has permission to delete a user object.

        Args:
            request: The HTTP request object.
            obj (NilvaUser): The user object being deleted.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        if obj is not None and request.user.permissions == NilvaUser.ADMIN:
            return True  # Admin users can delete any user object
        return False  # Normal users do not have delete permissions


admin.site.register(NilvaUser, NilvaUserAdmin)
