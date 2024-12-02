from django.contrib import admin

from user.models import ExerciseRPEOveride, Profile1RM, Program, ProgramDayV2


@admin.action(description="Create Templates for Program")
def make_hevy_templates_for_program(modeladmin, request, queryset):
    pass


@admin.action(description="Create Template for Program Day")
def make_hevy_templates_for_program_day(modeladmin, request, queryset):
    pass


@admin.register(Profile1RM)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ["user__username"]


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    search_fields = ["user__username"]
    actions = [make_hevy_templates_for_program]


@admin.register(ProgramDayV2)
class ProgramDayAdmin(admin.ModelAdmin):
    search_fields = ["user__username"]
    actions = [make_hevy_templates_for_program_day]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ExerciseRPEOveride)
class ExerciseRPEOverideAdmin(admin.ModelAdmin):
    search_fields = ["user"]
    autocomplete_fields = ["user", "exercise"]
