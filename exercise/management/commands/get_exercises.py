import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from exercise.models import BodyPart, Category
from exercise.models import Info as Exercise


class Command(BaseCommand):
    help = "Copies exercises from hevy app"

    def handle(self, *args, **options):
        limit = 100
        page = 1
        while response := requests.get(
            f"https://api.hevyapp.com/v1/exercise_templates?page={page}&pageSize={limit}",
            headers={
                "accept": "application/json",
                "api-key": settings.HEVY_API_KEY,
            },
        ):
            if response.status_code != 200:
                raise CommandError(
                    "got bad response %s" % response.status_code
                )
            page += 1

            for exercise in response.json()["exercise_templates"]:
                self.stdout.write(
                    self.style.NOTICE(
                        "writing exercise %s" % exercise["title"]
                    )
                )

                category, _ = Category.objects.get_or_create(
                    name=exercise["equipment"]
                )
                body_part, _ = BodyPart.objects.get_or_create(
                    name=exercise["primary_muscle_group"]
                )

                try:
                    Exercise.objects.get(name=exercise["title"])
                except Exercise.DoesNotExist:
                    Exercise.objects.create(
                        hevy_template_id=exercise["id"],
                        name=exercise["title"],
                        category=category,
                        body_part=body_part,
                    )

        self.stdout.write(
            self.style.SUCCESS("Successfully copied all exercises")
        )
