from django.contrib import admin

from user.models import Profile1RM


@admin.register(Profile1RM)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ["user__username"]

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return obj is None or obj.created_by == request.user
