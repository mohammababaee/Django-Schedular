from django.contrib import admin
from user.models import NilvaUser
from django.http.request import HttpRequest


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
        return qs.filter(
            id=request.user.id
        )  # Only current user profile if they were not admin

    def has_change_permission(self, request: HttpRequest, obj=None):

        if obj is not None and request.user.permissions == NilvaUser.ADMIN:
            return True  # True means admin user can change all profiles
        return (
            obj == request.user
        )  # Conditional: noraml user only can change their profile

    def has_delete_permission(self, request: HttpRequest, obj=None):
        if obj is not None and request.user.permissions == NilvaUser.ADMIN:
            return True  # Admin users can delete any user object
        return False  # Normal users do not have delete

    def has_add_permission(self, request: HttpRequest, obj=None):
        if request.user.permissions == NilvaUser.ADMIN:
            return True  # Admin users can add any user object
        return False  # Normal users do not have add permissions


admin.site.register(NilvaUser, NilvaUserAdmin)
