from django.contrib import admin
from .models import Task, NilvaUser


class TaskAdmin(admin.ModelAdmin):
    """
    Customizes the administration interface for the Task model.

    Methods:
        - get_queryset(self, request): Filters the queryset of tasks based on user permissions.
        - has_add_permission(self, request, obj=None): Checks if the user has permission to add a Task object.
    """

    list_filter = ("due_datetime", "title", "description")
    list_display = ("title", "description", "assigned_to", "due_datetime")

    def get_queryset(self, request):
        """
        Filters the queryset of tasks based on user permissions.

        Args:
            request: The HTTP request object.

        Returns:
            Queryset: Filtered queryset based on user permissions.
        """
        qs = super().get_queryset(request)
        if request.user.permissions == NilvaUser.ADMIN:
            return qs
        return qs.filter(assigned_to=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Customizes the form field for the assigned_to foreign key.

        Args:
            db_field: The ForeignKey field.
            request: The HTTP request object.
            kwargs: Additional keyword arguments.

        Returns:
            Field: Form field for the ForeignKey.
        """
        if (
            db_field.name == "assigned_to"
            and not request.user.permissions == NilvaUser.ADMIN
        ):
            kwargs["queryset"] = NilvaUser.objects.filter(pk=request.user.pk)
            kwargs["disabled"] = True
            kwargs["initial"] = request.user.pk
        elif (
            db_field.name == "assigned_to"
            and request.user.permissions == NilvaUser.ADMIN
        ):
            kwargs["queryset"] = NilvaUser.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Task, TaskAdmin)
