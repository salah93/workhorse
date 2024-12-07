import arrow
import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Get weeks total volume"

    def handle(self, *args, **options):
        LIMIT = 4
        response = requests.get(
            f"https://api.hevyapp.com/v1/workouts?pageSize={LIMIT}",
            headers={
                "accept": "application/json",
                "api-key": settings.HEVY_API_KEY,
            },
        )
        if response.status_code != 200:
            raise CommandError("got bad response %s" % response.status_code)

        now = arrow.utcnow()
        monday = now.shift(weekday=0, weeks=-1)  # Shift to last Monday

        workouts = [
            w
            for w in response.json()["workouts"]
            if arrow.get(w["created_at"]) >= monday
        ]
        total = 0
        for w in workouts:
            for e in w["exercises"]:
                for s in e["sets"]:
                    total += s["weight_kg"] * s["reps"]

        self.stdout.write(
            self.style.SUCCESS(f"Total volume = {total}kg, {monday} to {now}")
        )
