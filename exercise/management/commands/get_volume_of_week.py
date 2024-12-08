import arrow
import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Get weeks total volume"

    def add_arguments(self, parser):
        parser.add_argument("--weeks", default=1, type=int)
        parser.add_argument(
            "--start-of-week",
            dest="start",
            default=0,
            type=int,
            help="day of week, starting with monday - 0, and ending with sunday - 6",
        )

    def handle(self, *args, **options):
        LIMIT = 5

        curr_week = 1
        prev_weeks_workouts = []
        while curr_week <= options["weeks"]:
            now = arrow.utcnow().replace(hour=0, minute=0)
            start = now.shift(weekday=options["start"], weeks=-curr_week)
            end = start.shift(days=7)
            if end >= now:
                end = now
            self.stdout.write(
                self.style.NOTICE(
                    f"fetching for week {curr_week} {start.date()} to {end.date()}"
                )
            )

            response = requests.get(
                f"https://api.hevyapp.com/v1/workouts?page={curr_week}&pageSize={LIMIT}",
                headers={
                    "accept": "application/json",
                    "api-key": settings.HEVY_API_KEY,
                },
            )
            if response.status_code != 200:
                raise CommandError(
                    "got bad response %s" % response.status_code
                )

            curr_week += 1
            workouts = [
                w
                for w in response.json()["workouts"] + prev_weeks_workouts
                if arrow.get(w["start_time"]) >= start
                and arrow.get(w["start_time"]) <= end
            ]
            prev_weeks_workouts = [
                w
                for w in response.json()["workouts"]
                if w["id"] not in [r["id"] for r in workouts]
            ]
            total = 0
            for w in workouts:
                for e in w["exercises"]:
                    for s in e["sets"]:
                        if s["weight_kg"]:
                            total += s["weight_kg"] * s["reps"]

            self.stdout.write(
                self.style.SUCCESS(
                    f"Total volume = {total * 2.2} lb, - {len(workouts)} workouts"
                )
            )
