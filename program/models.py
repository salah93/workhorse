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

    def save(self):
        super().save()
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

    def save(self):
        if self.day > self.program.days_per_week:
            raise ValidationError("Day Exceeds days per week in program")
        if self.week > self.program.weeks:
            raise ValidationError("Week Exceeds weeks in program")
        super().save()

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
