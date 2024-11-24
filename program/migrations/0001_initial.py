# Generated by Django 5.1.3 on 2024-11-24 19:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Program",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                (
                    "weeks",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(4),
                            django.core.validators.MaxValueValidator(16),
                        ]
                    ),
                ),
                ("description", models.TextField()),
                (
                    "days_per_week",
                    models.IntegerField(
                        choices=[
                            (1, "One"),
                            (2, "Two"),
                            (3, "Three"),
                            (4, "Four"),
                            (5, "Five"),
                            (6, "Six"),
                            (7, "Seven"),
                        ]
                    ),
                ),
            ],
        ),
    ]