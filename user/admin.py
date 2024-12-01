from django.contrib import admin

from user.models import Profile1RM, Program


@admin.action(description="Create Templates for Program")
def make_strongapp_templates_for_program(modeladmin, request, queryset):
    pass


@admin.register(Profile1RM)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ["user__username"]


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    search_fields = ["user__username"]
    actions = [make_strongapp_templates_for_program]
