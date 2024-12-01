from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q


class DaysPerWeek(models.IntegerChoices):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7


class Reps(models.IntegerChoices):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10


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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        days = {(r.week, r.day) for r in self.day_set.all()}
        for w in range(1, self.weeks + 1):
            for d in range(1, self.days_per_week + 1):
                if (w, d) not in days:
                    Day.objects.create(program=self, week=w, day=d)
        self.day_set.filter(
            Q(week__gt=self.weeks) | Q(day__gt=self.days_per_week)
        ).delete()


class Day(models.Model):
    program = models.ForeignKey(Info, on_delete=models.CASCADE)
    week = models.PositiveSmallIntegerField()
    day = models.IntegerField(choices=DaysPerWeek)
    notes = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.day > self.program.days_per_week:
            raise ValidationError("Day Exceeds days per week in program")
        if self.week > self.program.weeks:
            raise ValidationError("Week Exceeds weeks in program")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Program Day"
        unique_together = [("program", "week", "day")]

    def __str__(self):
        return f"{self.program.name} - {self.week}.{self.day}"


class Exercise(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    exercise = models.ForeignKey("exercise.Info", on_delete=models.PROTECT)
    reps = models.PositiveSmallIntegerField(choices=Reps)
    sets = models.PositiveSmallIntegerField()
    rpe = models.FloatField(
        choices=[
            (6.5, 6.5),
            (7, 7),
            (7.5, 7.5),
            (8, 8),
            (8.5, 8.5),
            (9, 9),
            (9.5, 9.5),
            (10, 10),
        ],
        null=True,
        blank=True,
    )
    rpe_percentage = models.FloatField(
        validators=[MinValueValidator(60), MaxValueValidator(100)],
        null=True,
        blank=True,
    )
    is_superset = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)
    order = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "Program Exercise"
        unique_together = ("day", "order")

    def clean(self):
        if self.rpe and self.rpe_percentage:
            raise ValidationError(
                "Only one of rpe or rpe_percentage can be filled."
            )

    def __str__(self):
        return f"{self.day.program.name} - {self.day.week}.{self.day.day} - {self.exercise.name}"

    def get_rpe_percentage(self):
        rpe_map = {
            6.5: [
                0.88,
                0.85,
                0.82,
                0.80,
                0.77,
                0.75,
                0.72,
                0.69,
                0.67,
                0.64,
            ],
            7: [
                0.89,
                0.86,
                0.84,
                0.81,
                0.79,
                0.76,
                0.74,
                0.71,
                0.68,
                0.65,
            ],
            7.5: [
                0.91,
                0.88,
                0.85,
                0.82,
                0.80,
                0.77,
                0.75,
                0.72,
                0.69,
                0.67,
            ],
            8: [
                0.92,
                0.89,
                0.86,
                0.84,
                0.81,
                0.79,
                0.76,
                0.74,
                0.71,
                0.68,
            ],
            8.5: [
                0.94,
                0.91,
                0.88,
                0.85,
                0.82,
                0.80,
                0.77,
                0.75,
                0.72,
                0.69,
            ],
            9: [
                0.96,
                0.92,
                0.89,
                0.86,
                0.84,
                0.81,
                0.79,
                0.76,
                0.74,
                0.71,
            ],
            9.5: [
                0.98,
                0.94,
                0.91,
                0.88,
                0.85,
                0.82,
                0.80,
                0.77,
                0.75,
                0.72,
            ],
            10: [
                1,
                0.96,
                0.92,
                0.89,
                0.86,
                0.84,
                0.81,
                0.79,
                0.76,
                0.74,
            ],
        }
        return (
            self.rpe_percentage / 100
            if self.rpe_percentage
            else rpe_map[self.rpe][self.reps - 1]
        )
