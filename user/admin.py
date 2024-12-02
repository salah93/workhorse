from django.conf import settings
from django.contrib import admin, messages
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from user.models import ExerciseRPEOveride, Profile1RM, Program, ProgramDayV2

HEVY_API_HOST = "https://api.hevyapp.com"


def get_session():
    session = Session()
    retries = Retry(total=3, backoff_factor=0.1)
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session


@admin.action(description="Create Template for Program Day")
def make_hevy_templates_for_program_day(modeladmin, request, queryset):
    pass


@admin.register(Profile1RM)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ["user__username"]


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    search_fields = ["user__username"]
    actions = ["make_hevy_templates_for_program"]
    readonly_fields = ["hevy_routine_folder_id"]

    @admin.action(description="Create Templates for Program")
    def make_hevy_templates_for_program(self, request, queryset):
        session = get_session()
        incomplete_programs = []
        for program in queryset:
            response = session.post(
                f"{HEVY_API_HOST}/v1/routine_folders",
                data={"routine_folder": {"title": str(program.program)}},
                headers={
                    "accept": "application/json",
                    "api-key": settings.HEVY_API_KEY,
                },
            )
            if response.status_code != 201:
                incomplete_programs.append(program)
            else:
                program.hevy_routine_folder_id = response.json()[
                    "routine_folder"
                ]["id"]
                program.save()
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
