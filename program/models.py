from django.core.exceptions import ValidationError
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


class Info(models.Model):
    name = models.CharField(max_length=200, unique=True)
    weeks = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(4), MaxValueValidator(16)]
    )
    description = models.TextField()
    days_per_week = models.IntegerField(choices=DaysPerWeek)

    def __str__(self):
        return f"{self.name}"  # Or any other representation you prefer

    class Meta:
        verbose_name = "Program"


class Day(models.Model):
    program = models.ForeignKey(Info, on_delete=models.CASCADE)
    week = models.PositiveSmallIntegerField()
    day = models.IntegerField(choices=DaysPerWeek)
    notes = models.TextField()

    def clean(self):
        if self.day > self.program.days_per_week:
            raise ValidationError("Day Exceeds days per week in program")
        if self.week > self.program.weeks:
            raise ValidationError("Week Exceeds weeks in program")

    class Meta:
        verbose_name = "Program Day"
        unique_together = ("program", "week", "day")

    def __str__(self):
        return f"{self.program.name} - {self.week}.{self.day}"


class Exercise(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    exercise = models.ForeignKey("exercise.Info", on_delete=models.PROTECT)
    reps = models.PositiveSmallIntegerField()
    sets = models.PositiveSmallIntegerField()
    rpe_percentage = models.FloatField()
    is_superset = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "Program Exercise"
        unique_together = ("day", "order")

    def __str__(self):
        return f"{self.day.program.name} - {self.day.week}.{self.day.day} - {self.exercise.name}"
