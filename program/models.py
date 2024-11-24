from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class DaysPerWeek(models.IntegerChoices):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7


# Create your models here.
class Program(models.Model):
    name = models.CharField(max_length=200)
    weeks = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(4), MaxValueValidator(16)]
    )
    description = models.TextField()
    days_per_week = models.IntegerField(choices=DaysPerWeek)
