from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Profile1RM(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    squat = models.SmallIntegerField(
        validators=[MinValueValidator(45), MaxValueValidator(600)]
    )
    bench = models.SmallIntegerField(
        validators=[MinValueValidator(45), MaxValueValidator(600)]
    )
    deadlift = models.SmallIntegerField(
        validators=[MinValueValidator(45), MaxValueValidator(600)]
    )
    overhand_press = models.SmallIntegerField(
        validators=[MinValueValidator(45), MaxValueValidator(600)]
    )
    safety_squat_bar = models.SmallIntegerField(
        validators=[MinValueValidator(70), MaxValueValidator(600)]
    )

    class Meta:
        verbose_name = "Profile"

    def __str__(self):
        return f"{self.user.username}"


class Program(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    program = models.ForeignKey("program.Info", on_delete=models.CASCADE)
    hevy_routine_folder_id = models.CharField(
        max_length=10, unique=True, null=True
    )

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


class ProgramDayV2(models.Model):
    user_program = models.ForeignKey(Program, on_delete=models.CASCADE)
    program_day = models.ForeignKey("program.Day", on_delete=models.CASCADE)
    routine_link = models.CharField(max_length=100, null=True, unique=True)

    class Meta:
        verbose_name = "User Program Day"
        unique_together = [("user_program", "program_day")]

    def __str__(self):
        return f"{self.user_program.user.username} - {self.program_day}"

    def save(self, *args, **kwargs):
        if self.user_program.program != self.program_day.program:
            raise ValidationError("Programs do not match")
        super().save(*args, **kwargs)


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
