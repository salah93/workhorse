# Generated by Django 5.1.3 on 2024-12-01 00:33

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile1RM",
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
                (
                    "squat",
                    models.SmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(45),
                            django.core.validators.MaxValueValidator(600),
                        ]
                    ),
                ),
                (
                    "bench",
                    models.SmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(45),
                            django.core.validators.MaxValueValidator(600),
                        ]
                    ),
                ),
                (
                    "deadlift",
                    models.SmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(45),
                            django.core.validators.MaxValueValidator(600),
                        ]
                    ),
                ),
                (
                    "overhand_press",
                    models.SmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(45),
                            django.core.validators.MaxValueValidator(600),
                        ]
                    ),
                ),
                (
                    "safety_squat_bar",
                    models.SmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(70),
                            django.core.validators.MaxValueValidator(600),
                        ]
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
