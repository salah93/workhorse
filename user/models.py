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

    class Meta:
        verbose_name = "User Program"
        unique_together = [("user", "program")]

    def __str__(self):
        return f"{self.user.username} - {self.program}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for day in self.program.day_set.all():
            ProgramDayV2.objects.get_or_create(user=self, program_day=day)


class ProgramDayV2(models.Model):
    user_program = models.ForeignKey(Program, on_delete=models.CASCADE)
    program_day = models.ForeignKey("program.Day", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "User Program Day"
        unique_together = [("user_program", "program_day")]

    def __str__(self):
        return f"{self.user.username} - {self.program_day}"

    def save(self, *args, **kwargs):
        if self.user_program.program != self.program_day.program:
            raise ValidationError("Programs do not match")
        super().save(*args, **kwargs)
