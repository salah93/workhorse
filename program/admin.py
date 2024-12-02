from django.contrib import admin

from .models import Day, Exercise, Info


class DayAdminInline(admin.TabularInline):
    fields = ["notes"]
    model = Day

    def has_add_permission(self, request, obj):
        return False


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    fields = ["name", ("weeks", "days_per_week"), "description"]
    readonly_fields = ["hevy_routine_folder_id"]
    list_display = ["name"]
    inlines = [DayAdminInline]


class ExerciseInline(admin.TabularInline):
    model = Exercise
    autocomplete_fields = ["exercise"]


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    readonly_fields = ["program", "week", "day", "hevy_routine_id"]
    search_fields = ["program__name"]
    ordering = ["program__name", "week", "day"]
    inlines = [ExerciseInline]

    def has_add_permission(self, request):
        return False
