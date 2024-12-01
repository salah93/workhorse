from django.contrib import admin

from user.models import Profile1RM, Program, ProgramDay


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


@admin.register(ProgramDay)
class ProgramDayAdmin(admin.ModelAdmin):
    search_fields = ["user__username"]
    actions = [make_hevy_templates_for_program_day]
