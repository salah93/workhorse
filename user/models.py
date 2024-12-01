from django.contrib.auth.models import User
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
