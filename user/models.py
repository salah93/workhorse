from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

HEVY_API_HOST = "https://api.hevyapp.com"


def get_session():
    session = Session()
    retries = Retry(total=3, backoff_factor=0.1)
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session


class Profile1RM(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey("exercise.Info", on_delete=models.CASCADE)
    weight = models.SmallIntegerField(
        validators=[MinValueValidator(45), MaxValueValidator(600)]
    )

    class Meta:
        unique_together = [("user", "exercise")]
        verbose_name = "Profile"

    def __str__(self):
        return f"{self.user.username}"


class Program(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    program = models.ForeignKey("program.Info", on_delete=models.CASCADE)
    hevy_routine_folder_id = models.IntegerField(unique=True, null=True)

    class Meta:
        verbose_name = "User Program"
        unique_together = [("user", "program")]

    def __str__(self):
        return f"{self.user.username} - {self.program}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for day in self.program.day_set.all():
            ProgramDayV2.objects.get_or_create(
                user_program=self, program_day=day
            )

    def make_hevy_folder(self):
        session = get_session()
        success = True
        if self.hevy_routine_folder_id is None:
            response = session.post(
                f"{HEVY_API_HOST}/v1/routine_folders",
                json={"routine_folder": {"title": str(self.program)}},
                headers={
                    "accept": "application/json",
                    "api-key": settings.HEVY_API_KEY,
                },
            )
            success = response.status_code == 201
            if success:
                self.hevy_routine_folder_id = response.json()[
                    "routine_folder"
                ]["id"]
                self.save()
        return success

    def make_hevy_routines(self):
        for day in self.programdayv2_set.all():
            day.make_hevy_routine()


class ProgramDayV2(models.Model):
    user_program = models.ForeignKey(Program, on_delete=models.CASCADE)
    program_day = models.ForeignKey("program.Day", on_delete=models.CASCADE)
    hevy_routine_id = models.CharField(max_length=100, null=True, unique=True)

    class Meta:
        verbose_name = "User Program Day"
        unique_together = [("user_program", "program_day")]

    def __str__(self):
        return f"{self.user_program.user.username} - {self.program_day}"

    def save(self, *args, **kwargs):
        if self.user_program.program != self.program_day.program:
            raise ValidationError("Programs do not match")
        super().save(*args, **kwargs)

    def make_hevy_routine(self):
        session = get_session()
        success = True
        if self.hevy_routine_id is None:
            exercises = [
                {
                    "exercise_template_id": "D04AC939",
                    "superset_id": None,
                    "rest_seconds": 90,
                    "notes": "Stay slow and controlled.",
                    "sets": [
                        {
                            "type": "normal",
                            "weight_kg": 100,
                            "reps": 10,
                            "distance_meters": None,
                            "duration_seconds": None,
                        }
                    ],
                }
            ]
            response = session.post(
                f"{HEVY_API_HOST}/v1/routines",
                json={
                    "routine": {
                        "title": str(self.program_day),
                        "folder_id": self.user_program.hevy_routine_folder_id,
                        "notes": self.program_day.notes,
                        "exercises": exercises,
                    }
                },
                headers={
                    "accept": "application/json",
                    "api-key": settings.HEVY_API_KEY,
                },
            )
            success = response.status_code == 201
            if success:
                self.hevy_routine_folder_id = response.json()[
                    "routine_folder"
                ]["id"]
                self.save()
        return success


class ExerciseRPEOveride(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    exercise = models.ForeignKey("exercise.Info", on_delete=models.CASCADE)
    override_rpe_percentage = models.FloatField(
        validators=[MinValueValidator(60), MaxValueValidator(100)],
    )

    def __str__(self):
        return f"{self.user.username}"
