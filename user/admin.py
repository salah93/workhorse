from django.contrib import admin

from user.models import Profile1RM


@admin.register(Profile1RM)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ["user__username"]
