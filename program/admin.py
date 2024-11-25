from django.contrib import admin

from .models import Day, Exercise, Info


@admin.action(description="Create Templates for Program")
def make_strongapp_templates_for_program(modeladmin, request, queryset):
    pass


@admin.action(description="Create Template for Program Day")
def make_strongapp_template_for_day(modeladmin, request, queryset):
    pass


class DayAdminInline(admin.TabularInline):
    fields = ["notes"]
    model = Day

    def has_add_permission(self, request, obj):
        return False


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    fields = ["name", ("weeks", "days_per_week"), "description"]
    list_display = ["name"]
    actions = [make_strongapp_templates_for_program]
    inlines = [DayAdminInline]


class ExerciseInline(admin.TabularInline):
    model = Exercise


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    search_fields = ["program__name"]
    inlines = [ExerciseInline]
    actions = [make_strongapp_template_for_day]

    def has_add_permission(self, request):
        return False
