from django.db import models

# Create your models here.
class Program(models.Model):
    name = models.CharField(max_length=200)
    weeks = models.PositiveSmallIntegerField()
    description = models.TextField()
    days_per_week = models.PositiveSmallIntegerField(choices=range(1, 8))
