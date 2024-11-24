from django.contrib import admin

from .models import Info


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    fields = ["name", ("weeks", "days_per_week"), "description"]
    list_display = ["name"]
