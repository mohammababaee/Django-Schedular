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
            return qs  # Return all users to admin users
        return qs.filter(id=request.user.id)  # Only current user profile if they were not admin

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
            return True  # True means admin user can change all profiles
        return obj == request.user  # Conditional: noraml user only can change their profile

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
        return False  # Normal users do not have delete 
    def has_add_permission(self, request):
        """
        Checks if the user has permission to add a user object.

        Args:
            request: The HTTP request object.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        return request.user.permissions == NilvaUser.ADMIN


admin.site.register(NilvaUser, NilvaUserAdmin)
