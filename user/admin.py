from django.contrib import admin, messages

from user.models import ExerciseRPEOveride, Profile1RM, Program, ProgramDayV2


@admin.register(Profile1RM)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ["user__username"]
    autocomplete_fields = ["user", "exercise"]


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    search_fields = ["user__username"]
    actions = ["make_hevy_templates_for_program"]
    readonly_fields = ["hevy_routine_folder_id"]

    @admin.action(description="Create Templates for Program")
    def make_hevy_templates_for_program(self, request, queryset):
        incomplete_programs = []
        for program in queryset:
            success = program.make_hevy_folder()
            if not success:
                incomplete_programs.append(program)
            else:
                program.make_hevy_routines()
        if len(incomplete_programs):
            self.message_user(
                request,
                "Trouble updating following programs: %s"
                % incomplete_programs,
                messages.WARNING,
            )
        else:
            self.message_user(request, "Success !", messages.SUCCESS)


@admin.register(ProgramDayV2)
class ProgramDayAdmin(admin.ModelAdmin):
    search_fields = ["user__username"]
    readonly_fields = ["hevy_routine_id"]
    actions = ["make_hevy_template_for_program_day"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.action(description="Create Template for Program Day")
    def make_hevy_template_for_program_day(self, request, queryset):
        incomplete_routines = []
        for day in queryset:
            success = day.make_hevy_routine()
            if not success:
                incomplete_routines.append(day)
        if len(incomplete_routines):
            self.message_user(
                request,
                "Trouble updating following days: %s" % incomplete_routines,
                messages.WARNING,
            )
        else:
            self.message_user(request, "Success !", messages.SUCCESS)


@admin.register(ExerciseRPEOveride)
class ExerciseRPEOverideAdmin(admin.ModelAdmin):
    search_fields = ["user"]
    autocomplete_fields = ["user", "exercise"]
